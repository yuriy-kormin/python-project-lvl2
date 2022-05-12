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
        if set_status:
            property['status'] = statuses[set_status]
        return property['status'] if 'status' in property.keys() else None


def set_status_removed(property):
    status(property, set_status='-')


def set_status_added(property):
    status(property, set_status='+')


def set_status_equals(property):
    status(property, set_status='=')


def set_status_updated(property):
    status(property, set_status='!=')


def is_equals(property1, property2):
    properties = (property1, property2)
    if all(map(is_dir, properties)):
        return True
    elif all(map(is_record, properties)):
        if get_value(property1) == get_value(property2):
            return True
    return False


def find_diff(data1, data2):
    print("data1 inner:", data1,'\n\n')
    print("data2 inner:", data2,'\n\n')
    diff = {'children': {}}
    children_1 = get_children(data1)
    children_2 = get_children(data2)
    keys = children_1 | children_2
    for key in keys:
        # print(key)
        diff['children'][key] = children_2[key] if key in children_2.keys() else children_1[key]
        if key not in children_2.keys():
            set_status_removed(diff['children'][key])
        elif key not in children_1.keys():
            set_status_added(diff['children'][key])
        elif is_equals(children_1[key], children_2[key]):
            set_status_equals(diff['children'][key])
            if is_dir(diff['children'][key]):
                diff = find_diff(children_1[key], children_2[key])
            # set_old_record(diff[key], data1[key])
        else:
            set_status_updated(diff['children'][key])
            set_old_record(diff['children'][key], children_1[key])
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
#if it run - it's mean, that property is dir
    result = []
    for i, name in enumerate(data):
        result.append({'name': name})
        if isinstance(data[name], dict):
            result[i]['children'] = make_inner_format(data[name])
        else:
            result[i]['value'] = data[name]
    return result
