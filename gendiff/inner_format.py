from gendiff.statuses import statuses


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
    return property['old']


def get_children(property):
    return property['children'] if 'children' in property.keys() else {}


def status(property, set_status=None):

    # set_status: set status if isset else return existing status
    if isinstance(property, dict):
        if set_status and set_status in statuses:
            property['status'] = statuses[set_status]
        return property['status'] if 'status' in property.keys() else None


def is_equals(property1, property2):
    properties = (property1, property2)
    if all(map(is_dir, properties)):
        return True
    elif all(map(is_record, properties)):
        if get_value(property1) == get_value(property2):
            return True
    return False


def find_diff(data1, data2):
    # print ('diff ---  ')
    # print (data2)
    diff = {'children': {}}
    children_1 = get_children(data1)
    children_2 = get_children(data2)
    keys = children_1 | children_2
    for key in keys:
        diff['children'][key] = children_2[key] if key in children_2.keys() \
            else children_1[key]
        if key not in children_2.keys():
            status(diff['children'][key], set_status='-')
        elif key not in children_1.keys():
            status(diff['children'][key], set_status='+')
        elif is_equals(children_1[key], children_2[key]):
            status(diff['children'][key], set_status='=')
            if is_dir(diff['children'][key]):
                diff = find_diff(children_1[key], children_2[key])
        else:
            status(diff['children'][key], set_status='!=')
            set_old_record(diff['children'][key], children_1[key])
    return diff


def make_inner_format(data):
    result = {'children': {}}
    for name in data:
        if isinstance(data[name], dict):
            result['children'][name] = make_inner_format(data[name])
        else:
            result['children'][name] = {}
            result['children'][name]['value'] = data[name]
    return result
