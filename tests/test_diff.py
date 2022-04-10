import pytest
from gendiff import generate_diff
from gendiff.formatters.stylish import stylish


checking_data = ([['tests/fixtures/file1.yml',
                  'tests/fixtures/file2.yml'],
                 'tests/fixtures/output.txt'],
                 [['tests/fixtures/file1.json',
                   'tests/fixtures/file2.json'],
                  'tests/fixtures/output.txt'],
                 [['tests/fixtures/file1_nested.json',
                   'tests/fixtures/file2_nested.json'],
                  'tests/fixtures/output_nested.json'],
                 [['tests/fixtures/file1_nested.yml',
                   'tests/fixtures/file2_nested.yml'],
                  'tests/fixtures/out_nested.yml'])


@pytest.fixture
def right_result(path):
    with open(path) as rr_file:
        rr_lines = rr_file.readlines()
    return "".join(rr_lines)


@pytest.mark.parametrize('file_paths, path', checking_data)
def test_stylish(right_result, file_paths):
    result = stylish(generate_diff(file_paths[0], file_paths[1]))
    assert right_result == result
