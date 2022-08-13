from gendiff.file_parser import get_data
from gendiff.tree import build
from gendiff.formatter import formatting


def generate_diff(file_path1, file_path2, format_name='stylish'):
    diff = build(get_data(file_path1), get_data(file_path2))
    return formatting(format_name)(diff)
