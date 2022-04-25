from gendiff.inner_format import convert_path, get_status, get_name,\
    get_records_in_branch, is_dir, is_change_type
from gendiff.statuses import statuses

plain_statuses = {
    statuses['+']: 'added',
    statuses['-']: 'removed',
    statuses['!=']: 'updated'
}


def make_format_out(value):
    # print('type is' + str(type(value))+ '  val = '+str(value))
    if isinstance(value, bool):
        return str(value).lower()
    return '\'' + str(value) + '\''


def get_plain_value(id, data):
    if is_change_type(id, data):
        if data[id]['change_type_to'] == 'dir':
            return [make_format_out(data[id]['old_value']), '[complex value]']
        return ['[complex value]', make_format_out(data[id]['new_value'])]
    if get_status(id, data) == statuses['+']:
        return [make_format_out(data[id]['value']), None]
    return [make_format_out(data[id]['old_value']),
            make_format_out(data[id]['new_value'])]


def remove_root_element(list_):
    return list_[1:]


def make_string(id, data):
    path = remove_root_element(convert_path(id, data))
    # print (path)
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
    # print (data)

    def inner(id, data, mark=True):
        mark_status = mark
        result = []
        for record in get_records_in_branch(id, data):
            if get_status(record, data) != statuses['=']:
                if is_dir(record, data):
                    result.extend(inner(record, data, mark_status))
                else:
                    result.append(make_string(record, data))
        return result

        # sorted_records = sorted(records.items(), key=lambda x: x[1]['name'])
    return "\n".join(inner(0, data))
