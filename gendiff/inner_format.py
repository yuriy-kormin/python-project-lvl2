from gendiff.statuses import statuses


def get_name(property):
    if isinstance(property, dict) and 'name' in property.keys():
        return str(property['name'])
    return ''


def get_names(list_properties):
    return map(get_name, list_properties)


def is_dir(property):
    return isinstance(property, dict) and 'children' in property.keys()
    #     return True
    # return False


def is_record(property):
    return isinstance(property, dict) and 'value' in property.keys()
    #     return True
    # return False


def get_value(property):
    return property['value'] if is_record(property) else None


def set_value(property, value):
    if is_record(property):
        property['value'] = value


def set_old_record(property, record):
    property['old'] = record


def get_old_record(property):
    if 'old' in property.keys():
        result = property['old'].copy()
        set_status(result, '-')
        return result


def get_children(property, sorted_ = False):
    print ('get children for', property)
    if is_dir(property):
        result = property['children']
    elif is_record(property) or isinstance(property,list):
        result = property
    # print ('result is ',result)
    return sorted(result, key=lambda x: x['name']) if sorted_ else result


def set_children(property, children):
    property['children'] = children


def get_status(property):
    if isinstance(property, dict):
        return property['status'] if 'status' in property.keys() else ''
    return ''


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
    diff = []
    ids_in_data1 = [i for i in range(len(data1))]
    for i, child in enumerate(data2):
        diff.append(child.copy())
        id_in_data1 = get_id_by_name(get_name(child), data1)
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


def make_inner_format(data):
    result = []
    for i, name in enumerate(data):
        result.append({'name': name})
        if isinstance(data[name], dict):
            result[i]['children'] = make_inner_format(data[name])
        else:
            result[i]['value'] = data[name]
    return result
