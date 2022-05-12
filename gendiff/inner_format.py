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
    return property['children'] if 'children' in property.keys() else []


def set_children(property, children):
    property['children'] = children


def get_status(property):
    return property['status'] if 'status' in property.keys() else None


def set_status(property, status):
    if status in statuses:
        property['status'] = statuses[status]


def get_id_by_name(name, list_properties):
    for i, value in enumerate(list_properties):
        if get_name(value) == name:
            return i


def is_equals(*properties):
    if all(map(is_dir, properties)) or \
            (all(map(is_record, properties))
             and all(x == get_value(properties[0])
                     for x in map(get_value, properties))):
        return True
    return False


def find_diff(data1, data2):
    # print("data1 inner:", data1)
    # print("data2 inner:", data2,"\n")
    diff = []
    ids_in_data1 = [i for i in range(len(data1))]
    # print ('ids is ',ids_in_data1)
    for i, child in enumerate(data2):
        diff.append(child.copy())
        id_in_data1 = get_id_by_name(get_name(child), data1)
        # print (get_name(child),id_in_data1)
        if id_in_data1 is None:
            set_status(diff[i], '+')
        else:
            ids_in_data1.remove(id_in_data1)
            if is_equals(child, data1[id_in_data1]):
                set_status(diff[i], '=')
                if is_dir(diff[i]):
                    set_children(diff[i],
                                 find_diff(get_children(data1[id_in_data1]),
                                           get_children(child)))
            else:
                set_old_record(diff[i], data1[id_in_data1])
                set_status(diff[i], '!=')
    for i in ids_in_data1:
        cur_property = (data1[i].copy())
        set_status(cur_property, '-')
        diff.append(cur_property)
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
