def build_diff(data1, data2):
    result = []
    keys = data1.keys() | data2.keys()
    for key in sorted(keys):
        cur_node = {'key': key}
        if key not in data2:
            cur_node['type'] = 'removed'
            cur_node['value'] = data1[key]
        elif key not in data1:
            cur_node['type'] = 'added'
            cur_node['value'] = data2[key]
        elif type(data1[key]) == dict and type(data2[key]) == dict:
            cur_node['type'] = 'nested'
            cur_node['children'] = build_diff(data1[key], data2[key])
        elif data1[key] == data2[key]:
            cur_node['type'] = 'equals'
            cur_node['value'] = data1[key]
        else:
            cur_node['type'] = 'updated'
            cur_node['value'] = data1[key]
            cur_node['new_value'] = data2[key]
        result.append(cur_node)
    return result


def build(data1, data2):
    return {'type': 'root', 'children': build_diff(data1, data2)}


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
        if get_node_type(node) == 'updated' \
                and 'value' in node.keys() \
                and 'new_value' in node.keys():
            return node['value'], node['new_value']
        elif 'value' in node.keys():
            return node['value']
