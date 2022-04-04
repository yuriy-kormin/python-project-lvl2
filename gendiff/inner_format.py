import json
import yaml
import os
def get_parent_name(data, record):
    if data[record]['parent'] == 0:
        return 'root'
    parent_id = data[record]['parent']
    return data[parent_id]['name']


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


def get_record(data, record):
    answer = {}
    answer['name'] = data[record]['name']
    answer['value'] = data[record]['value']
    answer['parent'] = get_parent_name(data, record)
    children_names = get_children_names(data.data, record)
    if len(children_names):
        answer['childrens'] = children_names


def find_in_data2(record_data1_id, data1, data2):
    name = get_name(data1, record_data1_id)
    parent = get_parent_name(data1, record_data1_id)
    for i in data2:
        if name == get_name(data2, i) and parent == get_parent_name(data2, i):
            return i
    return 0


def find_diff(data1, data2):
    answer = {}
    for i in data1:
        answer[i] = data1[i]
        find_index = find_in_data2(i, data1, data2)
        if find_index:
            if 'value' in data1[i].keys():
                #это конечное значение
                if data1[i]['value'] == data2[find_index]['value']:
                    answer[i]['diff'] = 'equal'
                else:
                    answer[i]['diff'] = 'updated'
                    answer[i]['old_value'] = data1[i]['value']
                    answer[i]['new_value'] = data2[find_index]['value']
            else:
                answer[i]['diff'] = 'equal'
        else:
            answer[i]['diff'] = 'removed'
    for i in data2:
        if not find_in_data2(i, data2, data1):
            answer[i] = data2[i]
            answer[i]['diff'] = 'added'
    return answer


def make_inner_format(data, data_prev = None):
    id_count = 0
    result = {}

    def inner(data, id_count, result):
        parent_id = id_count
        children_ids = []
        for key in data:
            id_count += 1
            result[id_count] = {}
            result[id_count]['name'] = key
            result[id_count]['parent'] = parent_id
            children_ids.append(id_count)
            if isinstance(data[key], dict):
                result[id_count]['children'], id_count = inner(
                                                        data[key],
                                                        id_count,
                                                        result)
            else:
                result[id_count]['value'] = data[key]
        if data_prev is not None and id_count == 1:
            id_count = max(list(data_prev))
        return children_ids, id_count

    inner(data, id_count, result)
    return result

def convert_path(id, data):
    # print (data, ', id = ',id)
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


def checkin_data2(name, converted_path, check_data):
    for check_id in check_data:
        # print('get_name:', get_name(check_data, check_id), ', name:', name)

        # print('name:',name,'  path = ', str(converted_path))
        if get_name(check_data, check_id) == name and \
             convert_path(check_id, check_data) == converted_path:
            # print('founded')
            return check_id
    return None


def make_inner_format2(data, data_prev = None):
    id_count = 0 if not data_prev else max(data_prev)
    result = {}
    path = [0]

    def inner2(data, id_count, path):
        children_ids = []
        for key in data:
            if data_prev:
                converted_path = []
                for record in path:
                    converted_path.append(get_name(data_prev, record))
                # print ('path is ',str(path))
                checkin_id = checkin_data2(key, converted_path, data_prev) if data_prev else None
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
                result[checkin_id]['children'], id_count = inner2(
                    data[key],
                    id_count,
                    new_path)
            else:
                result[checkin_id]['value'] = data[key]
        return children_ids, id_count

    def inner(data, id_count, result, path):
        children_ids = []
        for key in data:
            id_count += 1
            result[id_count] = {}
            result[id_count]['name'] = key
            result[id_count]['path'] = path.copy()
            children_ids.append(id_count)
            if isinstance(data[key], dict):
                new_path = path.copy()
                new_path.append(id_count)
                result[id_count]['children'], id_count = inner(
                                                        data[key],
                                                        id_count,
                                                        result, new_path)
            else:
                result[id_count]['value'] = data[key]
        return children_ids, id_count

    inner2(data, id_count, path)

    return result


def read_file(file_path):
    type_file = os.path.splitext(file_path)[1]
    if type_file == '.yaml' or type_file == '.yml':
        parse_module = yaml.safe_load
    elif type_file == '.json':
        parse_module = json.load
    with open(file_path) as file_data:
        result = parse_module(file_data)
    return result


def read_files(*file_paths):
    result = []
    for file_path in file_paths:
        type_file = os.path.splitext(file_path)[1]
        if type_file == '.yaml' or type_file == '.yml':
            parse_module = yaml.safe_load
        elif type_file == '.json':
            parse_module = json.load
        with open(file_path) as file_data:
            result_append = parse_module(file_data)
        result.append(result_append)
    result = tuple(result)
    return result
