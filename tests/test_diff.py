import pytest
from gendiff import generate_diff

checking_files = (
    ('tests/fixtures/file1.yml', 'tests/fixtures/file2.yml'),
    ('tests/fixtures/file1.json', 'tests/fixtures/file2.json'),
    ('tests/fixtures/file1_nested.json', 'tests/fixtures/file2_nested.json'),
    ('tests/fixtures/file1_nested.yml', 'tests/fixtures/file2_nested.yml')
)
out_files_stylish = (
    'tests/fixtures/output.txt',
    'tests/fixtures/output.txt',
    'tests/fixtures/output_nested.json',
    'tests/fixtures/out_nested.yml'
)
out_files_plain = (
    'tests/fixtures/output_flat_plain.txt',
    'tests/fixtures/output_flat_plain.txt',
    'tests/fixtures/output_plain.txt',
    'tests/fixtures/output_nested_plain_yml.txt'
)

test_stylish = ((y, out_files_stylish[x]) for x, y in enumerate(checking_files))
test_plain = ([y, out_files_plain[x]] for x, y in enumerate(checking_files))


@pytest.fixture
def right_result(path):
    with open(path) as right_result_file:
        right_result_lines = right_result_file.readlines()
    return "".join(right_result_lines)


@pytest.mark.parametrize('file_paths,path', test_stylish)
def test_stylish(file_paths, right_result):
    result = generate_diff(file_paths[0], file_paths[1], 'stylish')
    assert right_result == result


@pytest.mark.parametrize('file_paths, path', test_plain)
def test_plain(file_paths, right_result):
    result = generate_diff(file_paths[0], file_paths[1], 'plain')
    assert right_result == result
