from gendiff.tree import get_node_name, get_node_type, get_node_children, \
    get_node_value


def render_stylish(data):
    children = get_node_children(data)
    result = []
    result.extend(node_processing(children))
    return "\n".join(result)


def build_indent(level, status=None):
    result = level * '    '
    if status:
        if status == 'added':
            return result + '  + '
        if status == 'removed':
            return result + '  - '
        if status == 'equals':
            return result + '    '
    return result


def node_processing(childrens, level=0, name=''):
    if not len(name):
        result = ['{']
    else:
        result = [build_indent(level) + name + ': {']
    for child in childrens:
        child_type = get_node_type(child)
        if child_type != 'nested':
            result.append(render_string(child, level))
        else:
            result.extend(node_processing(get_node_children(child), level + 1,
                                          get_node_name(child)))
    result.append(build_indent(level) + '}')
    return result


def render_string(child, level):
    status = get_node_type(child)
    answer = ''
    if status == 'updated':
        child_copy = child.copy()
        for cur_value in ('old_value', 'new_value'):
            child['type'] = 'removed' if cur_value == 'old_value' else 'added'
            child['value'] = child.pop(cur_value)
            answer += render_string(child, level)
            answer += '\n' if cur_value == 'old_value' else ''
        child = child_copy.copy()
    else:
        answer += build_indent(level, status) + get_node_name(child) \
            + ': ' + to_str(get_node_value(child), level)
    return answer


def to_str(data, level):
    if isinstance(data, bool):
        return str(data).lower()
    elif data is None:
        return 'null'
    elif isinstance(data, dict):
        level += 1
        result = ['{']
        for key in data.keys():
            if isinstance(data[key], dict):
                inner_dict = build_indent(level + 1) \
                    + key + ": " + to_str(data[key], level)
                result.append(inner_dict)
            else:
                cur_val = build_indent(level + 1) + key + ': ' \
                    + to_str(data[key], (level - 1))
                result.append(cur_val)
        result.append(build_indent(level) + '}')
        return "\n".join(result)
    return str(data)
