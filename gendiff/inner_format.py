from gendiff.statuses import statuses


def is_dir(id, data):
    checking_data = data if id is False else data[id]
    if 'children' in checking_data.keys():
        return True
    return False


def get_status(id, data):
    return data[id]['diff']


def is_change_type(id, data):
    if 'change_type_to' in data[id].keys():
        return True
    return False


def get_records_in_branch(id, data, sort_by_name=False):

    if id == 0:
        result = {x: data[x] for x in data if data[x]['path'] == [0]}
    elif id in data.keys():
        result = {x: data[x] for x in data[id]['children']}
    if sort_by_name:
        return {key: value for key, value in sorted(
            result.items(), key=lambda x: x[1]['name'])}
    return result


def get_name(id, data):
    if id in data.keys():
        return data[id]['name']
    elif id == 0:
        return 'root'
    return None


def find_diff(data1, data2):
    answer = {}
    for i in data1:
        answer[i] = data1[i]
        if get_name(i, data2):
            # If record exists in data2
            if is_dir(i, data1):
                if is_dir(i, data2):
                    '''if data1[key] and data2[key] is dir'''
                    answer[i]['diff'] = statuses['=']
                    answer[i]['children'].extend(
                        [x for x in data2[i]['children']
                         if x not in data1[i]['children']])
                else:
                    answer[i]['diff'] = statuses['!=']
                    answer[i]['change_type_to'] = 'value'
                    answer[i]['old_children'] = answer[i].pop('children')
                    answer[i]['new_value'] = data2[i]['value']
            else:
                if is_dir(i, data2):
                    answer[i]['diff'] = statuses['!=']
                    answer[i]['old_value'] = answer[i].pop('value')
                    answer[i]['change_type_to'] = 'dir'
                    answer[i]['new_children'] = data2[i]['children']
                else:
                    '''data1[key] and data2[key] is value'''
                    if data1[i]['value'] == data2[i]['value']:
                        answer[i]['diff'] = statuses['=']
                    else:
                        answer[i]['diff'] = statuses['!=']
                        answer[i]['old_value'] = data1[i]['value']
                        answer[i]['new_value'] = data2[i]['value']
        else:
            # if record do not exist in data2
            answer[i]['diff'] = statuses['-']
    for i in data2:
        if not get_name(i, data1):
            answer[i] = data2[i]
            answer[i]['diff'] = statuses['+']
    return answer


def convert_path(id, data):
    path = data[id]['path']
    answer = []
    for cur_id in path:
        answer.append(get_name(cur_id, data))
    return answer


def checkin_data(name, converted_path, check_data):
    for check_id in check_data:
        if get_name(check_id, check_data) == name and \
                convert_path(check_id, check_data) == converted_path:
            return check_id
    return None


def print_iv(data):
    for i in data:
        print('i=',i, ' data=',data[i])


def make_inner_format(data):
    ''' data_prev - first data to find properties in'''
    print_iv(data)
    print ('----')
    def inner(data):
        result = {}
        if isinstance((data), dict):
            result['children'] =[]
            for key in data:
                result['children'].append(inner(data[key]))
        else:
            result['value'] = data
        return result
    res = inner(data)
    print_iv(res)
    # id_count = 0 if not data_prev else max(data_prev)
    # result = {}
    # path = [0]
    #
    # def inner(data, id_count, path):
    #     children_ids = []
    #     for key in data:
    #         if data_prev:
    #             converted_path = []
    #             for record in path:
    #                 converted_path.append(get_name(record, data_prev))
    #             checkin_id = checkin_data(key, converted_path, data_prev) \
    #                 if data_prev else None
    #             if not checkin_id:
    #                 id_count += 1
    #                 checkin_id = id_count
    #         else:
    #             id_count += 1
    #             checkin_id = id_count
    #         result[checkin_id] = {}
    #         result[checkin_id]['name'] = key
    #         result[checkin_id]['path'] = path.copy()
    #         children_ids.append(checkin_id)
    #         if isinstance(data[key], dict):
    #             new_path = path.copy()
    #             new_path.append(checkin_id)
    #             result[checkin_id]['children'], id_count = inner(
    #                 data[key],
    #                 id_count,
    #                 new_path)
    #         else:
    #             result[checkin_id]['value'] = data[key]
    #     return children_ids, id_count
    #
    # inner(data, id_count, path)
    # return result
