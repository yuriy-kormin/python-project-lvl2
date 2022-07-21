from gendiff.statuses import statuses
from gendiff.tree import get_node_name,get_node_type,get_node_children,get_node_value


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


def make_block(childrens, level=0):
    result = ['{']
    for child in childrens:
        result.append(make_string(child, level))
    result.append('}')
    return result


def make_string(child, level=0):
    status = get_node_type(child)
    answer = ''
    if status in indents.keys():
        answer += level * indents[statuses['=']]
        answer += indents[status]
        answer += get_node_name(child) + ': '
        answer += normalize_output(get_node_value(child))
    elif status == statuses['!=']:
        child_copy = child.copy()
        child_copy['type'] = statuses['-']
        child_copy['value'] = child_copy['old']
        answer += make_string(child_copy, level) + '\n'
        child_copy['type'] = statuses['+']
        child_copy['value'] = child['value']
        answer += make_string(child_copy, level)
    return answer


def normalize_output(data):
    if isinstance(data, bool):
        return str(data).lower()
    elif data is None:
        return 'null'
    return str(data)