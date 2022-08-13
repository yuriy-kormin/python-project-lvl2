import os

from gendiff.parser import parse
from gendiff.tree import build
from gendiff.formatter import formatting


def generate_diff(file_path1, file_path2, format_name='stylish'):
    diff = build(get_data(file_path1), get_data(file_path2))
    return formatting(format_name)(diff)


def get_file_format(file_path):
    return os.path.splitext(file_path)[1][1:]


def get_data(file_path):
    file_format = get_file_format(file_path)
    with open(file_path) as file_data:
        return parse(file_data, file_format)
