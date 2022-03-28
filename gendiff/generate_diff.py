from gendiff import import_format


def make_out_format(data):
    return str(data).lower() if type(data) is bool else str(data)


def generate_diff(file_path1, file_path2):
    data_first_file, data_second_file = import_format.read_files(file_path1,
                                                                 file_path2)
    answer = "{\n"
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
    return answer
