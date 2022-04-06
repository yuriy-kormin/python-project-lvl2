from gendiff.inner_format import get_records_in_branch, is_dir
from gendiff.statuses import statuses


def make_out_format(data):
    if type(data) is bool:
        return str(data).lower()
    elif data is None:
        return 'null'
    else:
        return str(data)


def is_change_type_to(data):
    keys = data.keys()
    if 'change_type' in keys and data['change_type']:
        if 'old_value' in keys and 'children' in keys:
            return 'dir'
        if 'old_children' in keys and 'value' in keys:
            return 'value'
    return


def stylish(data):
    stylish_indents = {
        statuses['+']: '  + ',
        statuses['-']: '  - ',
        statuses['=']: '    '
    }

    def make_string(dict_, closed_line=False, mark=True):
        result = []
        print (dict_,mark)
        level = len(dict_['path']) - 1
        if closed_line:
            result.append(stylish_indents[statuses['=']] * level + '}')
        else:
            if dict_['diff'] == statuses['!=']:
                for diff_key in (statuses['-'], statuses['+']):
                    dict_['diff'] = diff_key
                    if not is_change_type_to(dict_):
                        if diff_key == statuses['-']:
                            dict_['value'] = dict_['old_value']
                        else:
                            dict_['value'] = dict_['new_value']
                    result.extend(make_string(dict_, False, mark))
            else:
                value = '{' if is_dir(False, dict_) else dict_['value']
                spaces = stylish_indents[dict_['diff']] if mark else stylish_indents[statuses['=']]
                print (spaces,':spaces')
                result.append(stylish_indents[statuses['=']] * level + \
                              spaces + dict_['name'] + ': ' + make_out_format(value))
        return result

    def inner(id, data, mark=True):
        mark_status = mark
        print(mark_status)
        result = []
        if id == 0:
            result.append('{')
        records = get_records_in_branch(id, data)
        print('records is ',records)
        sorted_records = sorted(records.items(), key=lambda x: x[1]['name'])
        for child in sorted_records:
            # print (child[1]['name'], mark_status)
            if is_change_type_to(child[1]) == 'dir':
                child[1]['value'] = child[1]['old_value']
            elif is_change_type_to(child[1]) == 'value':
                child[1]['children'] = child[1]['old_children']

            result.extend(make_string(child[1],mark = mark_status))
            if is_dir(False, child[1]):
                if child[1]['diff'] != statuses['=']:
                    mark_status = False
                    # pass
                print (' this is dir. mark status is ', mark_status)
                result.extend(inner(child[0], data, mark=mark_status))
                mark_status = mark
        result.extend(make_string(sorted_records[-1][1], closed_line=True, mark = mark_status))
        return result

    res = inner(0, data)
    return "\n".join(res)
