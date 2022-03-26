import pytest
from gendiff import generate_diff
from gendiff.scripts.gendiff import main
from unittest.mock import patch

right_result_path = 'tests/fixtures/output.txt'
output_help_path = 'tests/fixtures/help_output.txt'


@pytest.fixture
def right_result():
    with open(right_result_path) as right_result_file:
        result_lines = right_result_file.readlines()
    return "".join(result_lines)
#
# def test_help(capsys):
#     with open(output_help_path) as right_result_file:
#         result_lines = right_result_file.readlines()
#     right_result = ''.join(result_lines)
#     assert eval('gendiff -h') == right_result

def test_step4(right_result):
    result = generate_diff('tests/fixtures/file1.json',
                           'tests/fixtures/file2.json')
    assert right_result == result
