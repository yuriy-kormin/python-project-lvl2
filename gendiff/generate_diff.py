from gendiff.inner_format import make_inner_format, find_diff
from gendiff.file_parser import read_file
from gendiff.formatters.formatters import FORMATS


def generate_diff(file_path1, file_path2, format_name='plain'):
    data1 = make_inner_format(read_file(file_path1))
    data2 = make_inner_format(read_file(file_path2))
    diff = find_diff(data1, data2)
    return FORMATS[format_name](diff)
