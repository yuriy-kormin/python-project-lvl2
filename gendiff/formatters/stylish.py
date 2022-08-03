from gendiff.tree import get_node_name, get_node_type, get_node_children, \
    get_node_value

indents = {
    'added': '  + ',
    'removed': '  - ',
    'equals': '    ',
}


def make_format(data):
    children = get_node_children(data)
    result = []
    result.extend(make_block(children))
    return "\n".join(result)


def make_indent(level):
    return level * indents['equals']


def make_block(childrens, level=0, name=''):
    if not len(name):
        result = ['{']
    else:
        result = [make_indent(level) + name + ': {']
    for child in childrens:
        child_type = get_node_type(child)
        if child_type != 'nested':
            result.append(make_string(child, level))
        else:
            result.extend(make_block(get_node_children(child), level + 1,
                                     get_node_name(child)))
    result.append(make_indent(level) + '}')
    return result


def make_string(child, level):
    status = get_node_type(child)
    answer = ''
    if status in indents.keys():
        answer += make_indent(level) + indents[status] + get_node_name(child) \
            + ': ' + normalize_output(get_node_value(child), level)
    elif status == 'updated':
        child_copy = child.copy()
        for cur_value in ('old_value', 'new_value'):
            child['type'] = 'removed' if cur_value == 'old_value' else 'added'
            child['value'] = child.pop(cur_value)
            answer += make_string(child, level)
            answer += '\n' if cur_value == 'old_value' else ''
        child = child_copy.copy()
    return answer


def normalize_output(data, level):
    if isinstance(data, bool):
        return str(data).lower()
    elif data is None:
        return 'null'
    elif isinstance(data, dict):
        level += 1
        result = ['{']
        for key in data.keys():
            if isinstance(data[key], dict):
                inner_dict = make_indent(level + 1) \
                    + key + ": " + normalize_output(data[key], level)
                result.append(inner_dict)
            else:
                cur_val = make_indent(level + 1) + key + ': ' \
                    + normalize_output(data[key], (level - 1))
                result.append(cur_val)
        result.append(make_indent(level) + '}')
        return "\n".join(result)
    return str(data)
