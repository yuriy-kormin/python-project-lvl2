from gendiff.statuses import statuses
from gendiff.tree import get_node_name, get_node_type, get_node_children, \
    get_node_value

indents = {
    statuses['+']: '  + ',
    statuses['-']: '  - ',
    statuses['=']: '    ',
}


def make_format(data):
    children = get_node_children(data)
    result = []
    result.extend(make_block(children))
    return "\n".join(result)


def make_block(childrens, level=0, name=''):
    if not len(name):
        result = ['{']
    else:
        result = [level * indents[statuses['=']] + name + ': {']
    for child in childrens:
        child_type = get_node_type(child)
        if child_type != statuses['>']:
            result.append(make_string(child, level))
        else:
            result.extend(make_block(get_node_children(child), level + 1,
                                     get_node_name(child)))
    result.append(level * indents[statuses['=']] + '}')
    return result


def make_string(child, level):
    status = get_node_type(child)
    answer = ''
    if status in indents.keys():
        answer += level * indents[statuses['=']] + indents[status] \
            + get_node_name(child) + ': ' + normalize_output(
                                        get_node_value(child), level)
    elif status == statuses['!=']:
        child_copy = child.copy()
        child_copy['type'] = statuses['-']
        answer += make_string(child_copy, level) + '\n'
        child_copy['type'] = statuses['+']
        child_copy['value'] = child.pop('new_value')
        answer += make_string(child_copy, level)
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
                result.append(
                    indents[statuses['=']] * (level + 1) + key +
                    ": " + normalize_output(data[key], level)
                )
            else:
                result.append(
                    indents[statuses['=']] * (level + 1) + key + ': '
                    + normalize_output(data[key], (level - 1)))
        result.append(indents[statuses['=']] * level + '}')
        return "\n".join(result)
    return str(data)
