#!/usr/bin/env python3
import argparse
from gendiff import generate_diff
from gendiff.formatters.formatters import FORMATS


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '-f', '--format',
        type=str,
        help='set format of output_stylish',
        choices=FORMATS.keys(),
        default='stylish'
    )
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file, args.format)
    print(f'{diff}')


if __name__ == '__main__':
    main()
