import pytest
from gendiff import generate_diff
from gendiff.formatters.stylish import stylish

right_result_path = 'tests/fixtures/output.txt'
right_result_flat_path = 'tests/fixtures/output.txt'
right_result_nested_path = 'tests/fixtures/output_nested.json'
right_result_nestedYML_path = 'tests/fixtures/out_nested.yml'


checking_data = (
                [
                    ['tests/fixtures/file1.yml', 'tests/fixtures/file2.yml'],
                    'tests/fixtures/output.txt'
                ],
                [
                    ['tests/fixtures/file1.json', 'tests/fixtures/file2.json'],
                    'tests/fixtures/output.txt'
                ],
                [
                    ['tests/fixtures/file1_nested.json', 'tests/fixtures/file2_nested.json'],
                    'tests/fixtures/output_nested.json'
                ],
                [
                    ['tests/fixtures/file1_nested.yml', 'tests/fixtures/file2_nested.yml'],
                    'tests/fixtures/out_nested.yml'
                ]
)


@pytest.fixture
def rr(path):
    with open(path) as rr_file:
        rr_lines = rr_file.readlines()
    return "".join(rr_lines)


@pytest.mark.parametrize('file_paths, path', checking_data)
def test_stylish(rr, file_paths):
    result = stylish(generate_diff(file_paths[0], file_paths[1]))
    assert rr == result
