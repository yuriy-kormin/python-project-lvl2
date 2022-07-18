from gendiff.inner_format import make_inner_format, find_diff
from gendiff.file_parser import get_data
from gendiff.formatters.formatters import FORMATS


def generate_diff(file_path1, file_path2, format_name='stylish'):
    data1 = make_inner_format(get_data(file_path1))
    data2 = make_inner_format(get_data(file_path2))
    diff = find_diff(data1, data2)
    return FORMATS[format_name](diff)
