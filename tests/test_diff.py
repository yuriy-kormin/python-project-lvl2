import pytest
from gendiff import generate_diff

right_result_path = 'tests/fixtures/output.txt'


@pytest.fixture
def right_result():
    with open(right_result_path) as right_result_file:
        result_lines = right_result_file.readlines()
    return "".join(result_lines)


def test_xml(right_result):
    result = generate_diff('tests/fixtures/file1.json',
                           'tests/fixtures/file2.json')
    assert right_result == result


def test_yml(right_result):
    result = generate_diff('tests/fixtures/file1.yml',
                           'tests/fixtures/file2.yml')
    assert right_result == result
