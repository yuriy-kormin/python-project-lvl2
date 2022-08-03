from gendiff.tree import get_node_name, get_node_type, get_node_children, \
    get_node_value


def render_plain(data, path=''):
    result = []
    for child in get_node_children(data):
        if get_node_type(child) == 'nested':
            child_string = render_plain(
                child, path + get_node_name(child) + '.')
            if len(child_string):
                result.append(child_string)
        elif get_node_type(child) != 'equals':
            result.append(render_string(child, path))
    return '\n'.join(result)


def render_string(node, path=''):
    cur_status = get_node_type(node)
    name = path + get_node_name(node)
    answer = ''
    answer = 'Property \'' + name + '\' was ' + cur_status
    if cur_status == 'added':
        answer += ' with value: ' + to_str(get_node_value(node))
    elif cur_status == 'updated':
        old_value, new_value = tuple(map(to_str, get_node_value(node)))
        answer += '. From ' + old_value + ' to ' + new_value
    return answer


def to_str(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, int):
        return str(value)
    return '\'' + str(value) + '\''
