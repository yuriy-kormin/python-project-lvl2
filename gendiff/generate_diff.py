from gendiff import import_format



def make_inner_format(file_path1,file_path2):
    id_count = 0
    result = {}
    def inner(data,id_count,result):
        parent_id = id_count
        children_ids = []
        for key in data:
            id_count += 1
            result[id_count] = {}
            result[id_count]['name'] = key
            result[id_count]['parent'] = parent_id
            children_ids.append(id_count)
            if isinstance(data[key], dict):
                result[id_count]['children'] = inner(data[key],id_count,result)
            else:
                result[id_count]['children'] = False
        return children_ids
    data_first_file, data_second_file = import_format.read_files(file_path1,
                                                     file_path2)
    inner(data_first_file,id_count,result)
    print(result)


def make_out_format(data):
    return str(data).lower() if type(data) is bool else str(data)


def generate_diff(file_path1, file_path2):
    answer = "{\n"
    data_first_file, data_second_file = import_format.read_files(file_path1,
                                                                 file_path2)
    keys = sorted(data_first_file | data_second_file)
    for key in keys:
        prefix = ''

        if key in data_first_file:
            value_add = make_out_format(data_first_file[key])
            prefix = "-"
            if key in data_second_file and (
                    data_first_file[key] == data_second_file[key]):
                prefix = ' '
            answer += f'  {prefix} {key}: {value_add}\n'
        if key in data_second_file and prefix != ' ':
            value_add = make_out_format(data_second_file[key])
            prefix = '+'
            answer += f'  {prefix} {key}: {value_add}\n'
    answer += "}"
    make_inner_format(file_path1, file_path2)
    return answer




