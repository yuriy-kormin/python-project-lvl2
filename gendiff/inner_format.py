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


# def get_property(property):
#     return property
def set_old_record(property, record):
    property['old'] = record


def get_old_record(property):
    return property['old']


def get_children(root, property_name):
    if property_name in root.keys():
        if 'children' in root[property_name].keys():
            return root[property_name]['children']
    return {}
    # return property['children'] if 'children' in property.keys() else {}


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
    # print (data1)
    diff = {}
    for key in data1 | data2:
        # print(key)
        diff[key] = data2[key] if key in data2.keys() else data1[key]
        if key not in data2.keys():
            set_status_removed(diff[key])
        elif key not in data1.keys():
            set_status_added(diff[key])
        elif is_equals(data1[key], data2[key]):
            set_status_equals(diff[key])
            if is_dir(diff[key]):
                diff['children'] = find_diff(
                    get_children(data1, key),
                    get_children(data2, key)
                )
            # set_old_record(diff[key], data1[key])
        else:
            set_status_updated(diff[key])
            set_old_record(diff[key], data1[key])
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


def make_inner_format(source_data):
    # print('ORIG DATA')
    # print_iv(source_data)
    # print('----')

    def inner(data):
        result = {}
        for key in data:
            result[key] = {}
            if isinstance(data[key], dict):
                result[key]['children'] = inner(data[key])
            else:
                result[key]['value'] = data[key]
        return result

    return inner(source_data)
