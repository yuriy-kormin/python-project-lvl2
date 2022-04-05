#!/usr/bin/env python3
import argparse
from gendiff import generate_diff
from gendiff.formatters.stylish import stylish


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '--format',
        type=str,
        help='set format of output',
        choices=['stylish', 'json'],
        default='stylish'
    )
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)
    # print(stylish(diff))


if __name__ == '__main__':
    main()
