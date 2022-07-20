from gendiff.statuses import statuses
from gendiff.tree import get_node_name, get_node_type, get_node_children, get_node_value


def make_format(data, path=''):
    result = []
    for child in get_node_children(data):
        if get_node_type(child) == statuses['>']:
            child_string = make_format(child, path + get_node_name(child) + '.')
            if len(child_string):
                result.append(child_string)
        elif get_node_type(child) != statuses['=']:
            result.append(make_string(child, path))
    return '\n'.join(result)


def make_string(node, path=''):
    cur_status = get_node_type(node)
    name = path + get_node_name(node)
    answer = 'Property \'' + name + '\' was ' + cur_status
    if cur_status == statuses['+']:
        answer += ' with value: ' + normalize(get_node_value(node))
    elif cur_status == statuses['!=']:
        new_value, old_value = tuple(map(normalize, get_node_value(node)))
        answer += '. From ' + old_value + ' to ' + new_value
    return answer


def normalize(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, int):
        return str(value)
    return '\'' + str(value) + '\''
