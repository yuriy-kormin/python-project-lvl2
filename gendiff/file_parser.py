import json
import os
import yaml

from pyparsing import ParseException


def get_file_format(file_path):
    return os.path.splitext(file_path)[1][1:]


def parse(data, format_):
    if format_ in ('yaml', 'yml'):
        return yaml.safe_load
    elif format_ == 'json':
        return json.load
    raise ParseException('Unsupported file format')


def get_data(file_path):
    format_ = get_file_format(file_path)
    with open(file_path) as file_data:
        return parse(file_data, format_)
