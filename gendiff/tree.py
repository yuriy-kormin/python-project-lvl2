def build_diff(data1, data2):
    result = []
    keys = data1.keys() | data2.keys()
    for key in sorted(keys):
        if key not in data2:
            result.append({
                'key': key,
                'type': 'removed',
                'value': data1[key]
            })
        elif key not in data1:
            result.append({
                'key': key,
                'type': 'added',
                'value': data2[key]
            })
        elif type(data1[key]) == dict and type(data2[key]) == dict:
            result.append({
                'key': key,
                'type': 'nested',
                'children': build_diff(data1[key], data2[key])
            })
        elif data1[key] == data2[key]:
            result.append({
                'key': key,
                'type': 'equals',
                'value': data1[key]
            })
        else:
            result.append({
                'key': key,
                'type': 'updated',
                'old_value': data1[key],
                'new_value': data2[key]
            })
    return result


def build(data1, data2):
    return {'type': 'root', 'children': build_diff(data1, data2)}
