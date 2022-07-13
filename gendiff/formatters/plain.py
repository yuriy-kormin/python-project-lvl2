# from gendiff.inner_format import convert_path, get_status, get_name,\
#   get_records_in_branch, is_dir, is_change_type
from gendiff.inner_format import get_children, get_name, get_status, \
    is_dir, is_record, get_value, get_old_record
from gendiff.statuses import statuses

plain_statuses = {
    statuses['+']: 'added',
    statuses['-']: 'removed',
    statuses['!=']: 'updated'
}


def make_format_out(value):
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, int):
        return str(value)
    return '\'' + str(value) + '\''


def get_plain_value(property, old=False):
    value = get_old_record(property) if old else property
    if is_record(value):
        return make_format_out(get_value(value))
    return '[complex value]'


def make_string(property, path):
    cur_status = get_status(property)
    name = path + get_name(property)
    answer = 'Property \'' + name + '\' was ' + cur_status
    if cur_status == statuses['+']:
        answer += ' with value: ' + get_plain_value(property)
    elif cur_status == statuses['!=']:
        answer += '. From ' + get_plain_value(property, old=True) + \
                  ' to ' + get_plain_value(property)
    return answer


def make_format(data, path=''):
    result = []
    for child in get_children(data, sorted_=True):
        if is_dir(child):
            child_output = make_format(child, path + get_name(child) + '.')
            if len(child_output):
                result.append(child_output)
        if get_status(child) in plain_statuses:
            result.append(make_string(child, path))
    return '\n'.join(result)
