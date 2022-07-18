import json
import yaml
import os


def get_file_format(file_path):
    return os.path.splitext(file_path)[1]


def parse(data, format_):
    if format_ == '.yaml' or format_ == '.yml':
        parse_module = yaml.safe_load
    elif format_ == '.json':
        parse_module = json.load
    return parse_module(data)


def get_data(file_path):
    format_ = get_file_format(file_path)
    with open(file_path) as file_data:
        return parse(file_data, format_)
