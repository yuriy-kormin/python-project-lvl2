import pytest
from gendiff import generate_diff

checking_files = (
    ('tests/fixtures/file1.yml', 'tests/fixtures/file2.yml'),
    ('tests/fixtures/file1.json', 'tests/fixtures/file2.json'),
    ('tests/fixtures/file1_nested.json', 'tests/fixtures/file2_nested.json'),
    ('tests/fixtures/file1_nested.yml', 'tests/fixtures/file2_nested.yml')
)
out_files = (
    ('tests/fixtures/output.txt', 'tests/fixtures/output_flat_plain.txt'),
    ('tests/fixtures/output.txt', 'tests/fixtures/output_flat_plain.txt'),
    ('tests/fixtures/output_nested.json', 'tests/fixtures/output_plain.txt'),
    ('tests/fixtures/out_nested.yml', 'tests/fixtures/output_nested_plain_yml.txt')
)

test = [[y, out_files[x][0]] for x, y in enumerate(checking_files)]


@pytest.fixture
def right_result(path):
    with open(path) as right_result_file:
        right_result_lines = right_result_file.readlines()
    return "".join(right_result_lines)


# @pytest.mark.parametrize('file_paths', checking_files)
@pytest.mark.parametrize('file_paths, path', test)
def test_stylish(right_result, file_paths):
    result = generate_diff(file_paths[0], file_paths[1], 'stylish')
    assert right_result == result


test = [[y, out_files[x][1]] for x, y in enumerate(checking_files)]


@pytest.mark.parametrize('file_paths, path', test)
def test_stylish(right_result, file_paths):
    result = generate_diff(file_paths[0], file_paths[1], 'plain')
    assert right_result == result