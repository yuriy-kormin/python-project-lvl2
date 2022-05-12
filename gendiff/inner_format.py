from gendiff.statuses import statuses


def get_name(property):
    if isinstance(property, dict) and 'name' in property.keys():
        return property['name']


def get_names(list_properties):
    return map(get_name, list_properties)


def is_dir(property):
    if isinstance(property, dict) and 'children' in property.keys():
        return True
    return False


def is_record(property):
    if isinstance(property, dict) and 'value' in property.keys():
        return True
    return False


def get_value(property):
    return property['value'] if is_record(property) else None


def set_old_record(property, record):
    property['old'] = record


def get_old_record(property):
    return property['old'] if 'old' in property.keys() else None


def get_children(property):
    return property['children'] if isinstance(property, list) else []


def get_status(property):
    return property['status'] if 'status' in property.keys() else None


def set_status(property, status):
    if status in statuses:
        property['status'] = statuses[status]


def get_id_by_name(name, list_properties):
    for i, value in enumerate(list_properties):
        if get_name(value) == name:
            return i


def is_equals(property1, property2):
    if is_dir(property1):
        return True if is_dir(property2) else False
    elif is_record(property2) and get_value(property1) == get_value(property2):
        return True
    return False

    properties = (property1, property2)
    if all(map(is_dir, properties)):
        return True
    elif all(map(is_record, properties)):
        if get_value(property1) == get_value(property2):
            return True
    return False


def find_diff(data1, data2):
    print("data1 inner:", data1, '\n\n')
    print("data2 inner:", data2, '\n\n')
    diff = []
    ids_in_data2 = [i for i in range(len(data2))]
    for i, child in enumerate(data1):
        diff.append(child)
        id_in_data2 = get_id_by_name(get_name(child), data2)
        if id_in_data2 is not None:
            ids_in_data2.pop(id_in_data2)
            if is_equals(child, data2[id_in_data2]):
                set_status(diff[i], '=')
            else:
                set_status(diff[i], '!=')
                print ("set old ",child)
                set_old_record(diff[i], child)
        else:
            set_status(diff[i], '-')
    for i in ids_in_data2:
        cur_property = (data2[i])
        set_status(cur_property, '+')
        diff.append(cur_property)
        # diff.append()
        # # print(key)
        # diff['children'][key] = children_2[key] if key in children_2.keys() else children_1[key]
        # if key not in children_2.keys():
        #     set_status_removed(diff['children'][key])
        # elif key not in children_1.keys():
        #     set_status_added(diff['children'][key])
        # elif is_equals(children_1[key], children_2[key]):
        #     set_status_equals(diff['children'][key])
        #     if is_dir(diff['children'][key]):
        #         diff = find_diff(children_1[key], children_2[key])
        #     # set_old_record(diff[key], data1[key])
        # else:
        #     set_status_updated(diff['children'][key])
        #     set_old_record(diff['children'][key], children_1[key])
    return diff


def print_iv(data, sep=''):
    for i in data:
        if is_dir(data[i]):
            print(i, ':')
            print_iv(data[i]['children'], sep + ' ')
        else:
            string = ''
            for j in data[i]:
                string += str(j) + ':<' + str(data[i][j]) + '>, '
            print(sep + str(i), string)


def make_inner_format(data):
    # if it run - it's mean, that property is dir
    result = []
    for i, name in enumerate(data):
        result.append({'name': name})
        if isinstance(data[name], dict):
            result[i]['children'] = make_inner_format(data[name])
        else:
            result[i]['value'] = data[name]
    return result
