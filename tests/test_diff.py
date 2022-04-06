import pytest
from gendiff import generate_diff
from gendiff.formatters.stylish import stylish


right_result_path = 'tests/fixtures/output.txt'
right_result_nested_path = 'tests/fixtures/output_nested.json'

@pytest.fixture
def right_result_nested():
    with open(right_result_nested_path) as right_result_file:
        result_lines = right_result_file.readlines()
    return "".join(result_lines)


@pytest.fixture
def right_result():
    with open(right_result_path) as right_result_file:
        result_lines = right_result_file.readlines()
    return "".join(result_lines)


def test_xml(right_result):
    result = stylish(generate_diff('tests/fixtures/file1.json',
                           'tests/fixtures/file2.json'))
    assert right_result == result


def test_nested_xml(right_result_nested):
    result = stylish(generate_diff('tests/fixtures/file1_nested.json',
                           'tests/fixtures/file2_nested.json'))
    assert right_result_nested == result


def test_yml(right_result):
    result = stylish(generate_diff('tests/fixtures/file1.yml',
                           'tests/fixtures/file2.yml'))
    assert right_result == result
