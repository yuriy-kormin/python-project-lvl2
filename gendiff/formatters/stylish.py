from gendiff.inner_format import get_records_in_branch, is_dir
from gendiff.statuses import statuses


stylish_indents = {
                    statuses['+']: '  + ',
                    statuses['-']: '  - ',
                    statuses['=']: '    '
                  }


def make_out_format(data):
    answer = ''
    if type(data) is bool:
        answer = str(data).lower()
    elif data is None:
        answer = 'null'
    else:
        answer = str(data)
    return ' ' + answer if len(answer) else ''


def is_change_type_to(data):
    keys = data.keys()
    if 'change_type_to' in keys:
        return data['change_type_to']
    return None


def make_string(dict_, closed_line=False, mark=True):
    result = []
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
            spaces = stylish_indents[dict_['diff']] if mark \
                else stylish_indents[statuses['=']]
            result.append(stylish_indents[statuses['=']] * level +
                          spaces + dict_['name'] + ':' +
                          make_out_format(value))
    return result


def stylish(data):
    def inner(id, data, mark=True):
        mark_status = mark
        result = []
        if id == 0:
            result.append('{')
        records = get_records_in_branch(id, data)
        sorted_records = sorted(records.items(), key=lambda x: x[1]['name'])
        for child in sorted_records:
            if is_change_type_to(child[1]) == 'dir':
                child[1]['value'] = child[1]['old_value']
                child[1]['diff'] = statuses['-']
                result.extend(make_string(child[1], mark=mark_status))
                child[1].pop('value')
                child[1]['children'] = child[1]['new_children']
                child[1]['diff'] = statuses['+']
                result.extend(make_string(child[1], mark=mark_status))
                mark_status = False
                result.extend(inner(child[0], data, mark=mark_status))
                child[1].pop('children')
                mark_status = mark
            elif is_change_type_to(child[1]) == 'value':
                child[1]['children'] = child[1]['old_children']
                child[1]['diff'] = statuses['-']
                result.extend(make_string(child[1], mark=mark_status))
                mark_status = False
                result.extend(inner(child[0], data, mark=mark_status))
                mark_status = mark
                child[1].pop('children')
                child[1]['value'] = child[1]['new_value']
                child[1]['diff'] = statuses['+']
                result.extend(make_string(child[1], mark=mark_status))
                child[1].pop('value')
                mark_status = mark
            else:
                result.extend(make_string(child[1], mark=mark_status))
            if is_dir(False, child[1]):
                if child[1]['diff'] != statuses['=']:
                    mark_status = False
                result.extend(inner(child[0], data, mark=mark_status))
                mark_status = mark
        result.extend(
            make_string(sorted_records[-1][1],
                        closed_line=True,
                        mark=mark_status))
        return result
    res = inner(0, data)
    return "\n".join(res)
