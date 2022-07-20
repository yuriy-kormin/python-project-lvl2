from gendiff.statuses import statuses


def build_diff(data1, data2):
    result = []
    keys = data1.keys() | data2.keys()
    for key in sorted(keys):
        if key not in data2:
            result.append({
                'key': key,
                'type': statuses['-'],
                'value': data1[key]
            })
        elif key not in data1:
            result.append({
                'key': key,
                'type': statuses['+'],
                'value': data2[key]
            })
        elif type(data1[key]) == dict and type(data2[key]) == dict:
            result.append({
                'key': key,
                'type': statuses['>'],
                'children': build_diff(data1[key], data2[key])
            }),
        elif data1[key] == data2[key]:
            result.append({
                'key': key,
                'type': statuses['='],
                'value': data1[key]
            })
        else:
            result.append({
                'key': key,
                'type': statuses['!='],
                'value': data2[key],
                'old': data1[key]
            })
    return result


def build(data1, data2):
    return {'type': statuses['/'], 'children': build_diff(data1, data2)}


def get_node_name(node):
    if isinstance(node, dict) and 'key' in node.keys():
        return node['key']


def get_node_children(node):
    if isinstance(node, dict) and 'children' in node.keys():
        return node['children']


def get_node_type(node):
    if isinstance(node, dict) and 'type' in node.keys():
        return node['type']


def get_node_value(node):
    if isinstance(node, dict):
        if get_node_type(node) == statuses['!='] \
                and 'value' in node.keys() \
                and 'old' in node.keys():
            return node['value'], node['old']
        elif 'value' in node.keys():
            return node['value']
