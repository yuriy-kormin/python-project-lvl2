from gendiff.inner_format import get_records_in_branch


def make_out_format(data):
    if type(data) is bool:
        return str(data).lower()
    elif data is None:
        return 'null'
    else:
        return str(data)


def stylish(data):
    stylish_indents = {
        'added': '  + ',
        'removed': '  - ',
        'equal': '    '
    }

    def make_string(dict_, closed_line=False):
        result = []
        # print(dict_)
        level = len(dict_['path']) - 1
        if closed_line:
            result.append(stylish_indents['equal']*level + '}')
        else:
            if dict_['diff'] == 'updated':
                for diff_key in ('removed', 'added'):
                    dict_['diff'] = diff_key
                    if diff_key == 'removed':
                        dict_['value'] = dict_['old_value']
                    else:
                        dict_['value'] = dict_['new_value']
                    result.extend(make_string(dict_))
            else:
                value = dict_['value'] if 'value' in dict_.keys() else '{'
                result.append(stylish_indents['equal']*level+ \
                              stylish_indents[dict_['diff']] + \
                              dict_['name'] + ': ' + \
                              make_out_format(value))
        return result

    def inner(id, data):
        result = []
        if id == 0:
            result.append('{')
            records = get_records_in_branch(id, data)
            sorted_records = sorted(records.items(), key=lambda x: x[1]['name'])
            for child in sorted_records:
                result.extend(make_string(child[1]))
                if 'children' in child[1].keys():
                    result.extend(inner(child[0], data))
            result.extend(make_string(sorted_records[-1][1], closed_line=True))
        else:
            records = get_records_in_branch(id, data)
            sorted_records = sorted(records.items(), key=lambda x: x[1]['name'])
            print(records)
            for child in sorted_records:
                result.extend(make_string(child[1]))
            result.extend(make_string(sorted_records[-1][1], closed_line=True))
        return result

    res = inner(0, data)
    return "\n".join(res)
