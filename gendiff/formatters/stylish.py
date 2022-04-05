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
        'added':'  + ',
        'removed':'  - ',
        'equal':'    ',
        'updated':'  ~ ',
    }

    def make_string(dict_):
        result = []
        if dict_['diff'] != 'updated':
            result.append(stylish_indents[dict_['diff']] + \
                          dict_['name'] + ': ' + \
                          make_out_format(dict_['value']))
        else:
            for diff_key in ('removed','added'):
                dict_['diff'] = diff_key
                if diff_key == 'removed':
                    dict_['value'] = dict_['old_value']
                else:
                    dict_['value'] = dict_['new_value']
                result.extend(make_string(dict_))
        return result

    def inner(id, data):
        if id == 0:
            result = ['{']
            records = get_records_in_branch(id, data)
            for child in sorted(records.items(), key=lambda x: x[1]['name']):
                result.extend(make_string(child[1]))
            result.append('}')
        else:
            result = []
        return result
    res = inner(0,data)
    # print (res)
    return "\n".join(res)
