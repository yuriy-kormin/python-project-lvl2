#!/usr/bin/env python3
import argparse
import json


def generate_diff(file_path1, file_path2):
    answer = "{\n"
    with open(file_path1) as first_file:
        with open(file_path2) as second_file:
            data_first_file = json.load(first_file)
            data_second_file = json.load(second_file)
    keys = sorted(data_first_file | data_second_file)
    for key in keys:
        if key in data_first_file:
            prefix = "-"
            if (key in data_second_file and
                    data_first_file[key] == data_second_file[key]):
                prefix = ' '
            answer += f'  {prefix} {key}: {data_first_file[key]}\n'
        if key in data_second_file and prefix != ' ':
            prefix = '+'
            answer += f'  {prefix} {key}: {data_second_file[key]}\n'
    answer += "}"
    return answer


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '--format',
        type=str,
        help='set format of output',
        default='json'
    )
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
