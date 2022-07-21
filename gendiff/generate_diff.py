# from gendiff.inner_format import make_inner_format, find_diff
from gendiff.file_parser import get_data
from gendiff.tree import build
from gendiff.formatters.formatters import FORMATS


def generate_diff(file_path1, file_path2, format_name='stylish'):
    diff = build(get_data(file_path1), get_data(file_path2))
    if format_name in FORMATS:
        return FORMATS[format_name](diff)
    raise ValueError(f'Unknown format: {format_name}')
