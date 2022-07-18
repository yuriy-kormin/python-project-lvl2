import argparse
from gendiff.formatters.formatters import FORMATS


def parse_args():
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
    return parser.parse_args()
