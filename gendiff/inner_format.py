def get_parent_name(data, record):
    if data[record]['parent'] == 0:
        return 'root'
    parent_id = data[record]['parent']
    return data[parent_id]['name']


def is_dir(id, data):
    if 'children' in data[id].keys():
        return True
    return False


def get_children_names(data, record):
    answer = []
    if 'children' in data[record].keys():
        for child_id in data[record]['children']:
            answer.append(data[child_id]['name'])
    return answer


def get_name(data, record):
    # print (record, 'is record')
    if record in data.keys():
        return data[record]['name']
    elif record == 0:
        return 'root'
    return None


def find_diff(data1, data2):
    answer = {}
    for i in data1:
        answer[i] = data1[i]
        if get_name(data2, i):
            # If record exists in data2
            if is_dir(i, data1):
                if is_dir(i, data2):
                    #if data1[key] and data2[key] is dir
                    answer[i]['diff'] = 'equal'
                else:
                    answer[i]['diff'] = 'updated'
            else:
                #data1[key] is value
                if is_dir(i, data2):
                    answer[i]['diff'] = 'updated'
                else:
                    #data1[key] and data2[key] is value
                    if data1[i]['value'] == data2[i]['value']:
                        answer[i]['diff'] = 'equal'
                    else:
                        answer[i]['diff'] = 'updated'
        else:
            # if record does not exists in data2
            answer[i]['diff'] = 'removed'
    for i in data2:
        if not get_name(data1, i):
            answer[i] = data2[i]
            answer[i]['diff'] = 'added'
    return answer


def convert_path(id, data):
    path = data[id]['path']
    answer = []
    for cur_id in path:
        answer.append(get_name(data, cur_id))
    return answer


def convert_children(id, data):
    path = data[id]
    answer = []
    if 'children' in path.keys():
        path = data[id]['children']
        for cur_id in path:
            answer.append(get_name(data, cur_id))
    return answer


def checkin_data(name, converted_path, check_data):
    for check_id in check_data:
        # print('get_name:', get_name(check_data, check_id), ', name:', name)

        # print('name:',name,'  path = ', str(converted_path))
        if get_name(check_data, check_id) == name and \
             convert_path(check_id, check_data) == converted_path:
            # print('founded')
            return check_id
    return None


def make_inner_format(data, data_prev = None):
    id_count = 0 if not data_prev else max(data_prev)
    result = {}
    path = [0]

    def inner(data, id_count, path):
        children_ids = []
        for key in data:
            if data_prev:
                converted_path = []
                for record in path:
                    converted_path.append(get_name(data_prev, record))
                # print ('path is ',str(path))
                checkin_id = checkin_data(key, converted_path, data_prev) if data_prev else None
                # print ('checkin id ',checkin_id)
                if not checkin_id:
                    id_count += 1
                    checkin_id = id_count
            # print(result)
            else:
                id_count += 1
                checkin_id = id_count
            result[checkin_id] = {}
            # print("add record ", checkin_id)
            # print(result)
            result[checkin_id]['name'] = key
            result[checkin_id]['path'] = path.copy()
            children_ids.append(checkin_id)
            if isinstance(data[key], dict):
                new_path = path.copy()
                new_path.append(checkin_id)
                result[checkin_id]['children'], id_count = inner(
                    data[key],
                    id_count,
                    new_path)
            else:
                result[checkin_id]['value'] = data[key]
        return children_ids, id_count

    inner(data, id_count, path)
    return result

