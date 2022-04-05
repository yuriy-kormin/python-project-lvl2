import json
import yaml
import os


def read_file(file_path):
    type_file = os.path.splitext(file_path)[1]
    if type_file == '.yaml' or type_file == '.yml':
        parse_module = yaml.safe_load
    elif type_file == '.json':
        parse_module = json.load
    with open(file_path) as file_data:
        result = parse_module(file_data)
    return result
