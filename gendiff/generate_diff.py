from gendiff.inner_format import make_inner_format, find_diff
from gendiff.file_parser import read_file


def generate_diff(file_path1, file_path2):
    data1 = make_inner_format(read_file(file_path1))
    data2 = make_inner_format(read_file(file_path2), data1)
    return find_diff(data1, data2)
