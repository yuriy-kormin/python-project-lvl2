from gendiff.inner_format import make_inner_format, find_diff
from gendiff.file_parser import read_file


def make_out_format(data):
    return str(data).lower() if type(data) is bool else str(data)


def generate_diff(file_path1, file_path2):
    # answer = "{\n"
    # data_first_file, data_second_file = inner_format.read_files(file_path1,
    #                                                              file_path2)
    # keys = sorted(data_first_file | data_second_file)
    # for key in keys:
    #     prefix = ''
    #     if key in data_first_file:
    #         value_add = make_out_format(data_first_file[key])
    #         prefix = "-"
    #         if key in data_second_file and (
    #                 data_first_file[key] == data_second_file[key]):
    #             prefix = ' '
    #         answer += f'  {prefix} {key}: {value_add}\n'
    #     if key in data_second_file and prefix != ' ':
    #         value_add = make_out_format(data_second_file[key])
    #         prefix = '+'
    #         answer += f'  {prefix} {key}: {value_add}\n'
    # answer += "}"
    #
    # def get_var_name(variable):
    #     for name in globals():
    #         if eval(name) == variable and eval(name) is not None:
    #             return name
    #
    # def print_in(data):
    #     name_data = get_var_name(data)
    #     print('=' * 20, '    ',name_data,'   ', '=' * 20)
    #     for i in sorted(data):
    #         string = str(i) + ', '
    #         string += str(data[i]['name'])
    #         if 'diff' in data[i].keys():
    #             string+=' diff=' + data[i]['diff']
    #         # for key in data[i].keys():
    #             # string += key + ' "' + str(data[i][key]) + '" '
    #         # string += 'parents : ' + str(inner_format.convert_path(i, data))
    #         # children = inner_format.convert_children(i, data)
    #         # string += ', children : ' + str(children) if len(children) else ''
    #         print(string)
    #     print("-"*80)

    data1 = make_inner_format(read_file(file_path1))
    data2 = make_inner_format(read_file(file_path2), data1)
    diff = find_diff(data1, data2)
    return diff
