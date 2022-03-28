from gendiff import import_format


def generate_diff(file_path1, file_path2):
    data_first_file, data_second_file = import_format.read_files(file_path1,
                                                                 file_path2)
    answer = "{\n"
    keys = sorted(data_first_file | data_second_file)
    for key in keys:
        if key in data_first_file:
            prefix = "-"
            if key in data_second_file and (
                    data_first_file[key] == data_second_file[key]):
                prefix = ' '
            answer += f'  {prefix} {key}: {data_first_file[key]}\n'
        if key in data_second_file and prefix != ' ':
            prefix = '+'
            answer += f'  {prefix} {key}: {data_second_file[key]}\n'
    answer += "}"
    return answer
