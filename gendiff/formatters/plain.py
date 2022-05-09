# from gendiff.inner_format import convert_path, get_status, get_name,\
#   get_records_in_branch, is_dir, is_change_type
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
    return '\'' + str(value) + '\''


def get_plain_value(id, data):
    if is_change_type(id, data):
        if data[id]['change_type_to'] == 'dir':
            return [make_format_out(data[id]['old_value']), '[complex value]']
        return ['[complex value]', make_format_out(data[id]['new_value'])]
    if get_status(id, data) == statuses['+']:
        if is_dir(id, data):
            return ['[complex value]', None]
        return [make_format_out(data[id]['value']), None]
    return [make_format_out(data[id]['old_value']),
            make_format_out(data[id]['new_value'])]


def remove_root_element(list_):
    return list_[1:]


def make_string(id, data):
    path = remove_root_element(convert_path(id, data))
    path.append(get_name(id, data))
    answer = 'Property \'' + ".".join(path) + '\' was ' +\
             plain_statuses[get_status(id, data)]
    if get_status(id, data) == statuses['+']:
        answer += ' with value: ' + get_plain_value(id, data)[0]
    if get_status(id, data) == statuses['!=']:
        old_value, new_value = get_plain_value(id, data)
        answer += '. From ' + old_value + ' to ' + new_value
    return answer


def make_format(data):
    def inner(id, data):
        result = []
        sorted_records = get_records_in_branch(id, data, sort_by_name=True)
        for record in sorted_records:
            if get_status(record, data) != statuses['=']:
                result.append(make_string(record, data))
            elif is_dir(record, data):
                result.extend(inner(record, data))
        return result
    return "\n".join(inner(0, data))
