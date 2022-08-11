import json
import os
import yaml


def get_file_format(file_path):
    return os.path.splitext(file_path)[1][1:]


def parse(data, file_format):
    if file_format in ('yaml', 'yml'):
        return yaml.safe_load(data)
    elif file_format == 'json':
        return json.load(data)
    raise ValueError('Unsupported file format')


def get_data(file_path):
    file_format = get_file_format(file_path)
    with open(file_path) as file_data:
        return parse(file_data, file_format)
