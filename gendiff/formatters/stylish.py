from gendiff.inner_format import get_records_in_branch
from gendiff.statuses import statuses

def make_out_format(data):
    if type(data) is bool:
        return str(data).lower()
    elif data is None:
        return 'null'
    else:
        return str(data)


def stylish(data):
    stylish_indents = {
        statuses['+']: '  + ',
        statuses['-']: '  - ',
        statuses['=']: '    '
    }

    def make_string(dict_, closed_line=False):
        mark = True
        result = []
        level = len(dict_['path']) - 1
        if closed_line:
            result.append(stylish_indents[statuses['=']]*level + '}')
        else:
            # print ('diff', dict_['diff'])
            if dict_['diff'] == statuses['!=']:
                for diff_key in (statuses['-'], statuses['+']):
                    dict_['diff'] = diff_key
                    if diff_key == statuses['-']:
                        dict_['value'] = dict_['old_value']
                    else:
                        dict_['value'] = dict_['new_value']
                    result.extend(make_string(dict_))
            else:
                value = dict_['value'] if 'value' in dict_.keys() else '{'
                spaces = stylish_indents[dict_['diff']] if mark else stylish_indents[statuses['=']]
                result.append(stylish_indents[statuses['=']]*level+ \
                               spaces + \
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
            # if child[1]['diff'] == statuses['=']:
            result.extend(make_string(child[1]))
            if 'children' in child[1].keys():
                result.extend(inner(child[0], data))
        result.extend(make_string(sorted_records[-1][1], closed_line=True))
        return result

    res = inner(0, data)
    return "\n".join(res)
