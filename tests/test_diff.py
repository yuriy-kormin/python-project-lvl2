import pytest
from gendiff import generate_diff
from gendiff.formatters.stylish import stylish

right_result_path = 'tests/fixtures/output.txt'
right_result_flat_path = 'tests/fixtures/output.txt'
right_result_nested_path = 'tests/fixtures/output_nested.json'
right_result_nestedYML_path = 'tests/fixtures/out_nested.yml'


checking_data={
                  1:['tests/fixtures/file1.yml', 'tests/fixtures/file2.yml']

}


@pytest.fixture
def rr(path):
    with open(path) as rr_file:
        rr_lines = rr_file.readlines()
    return "".join(rr_lines)

@pytest.mark.parametrize('path', [right_result_flat_path])
def test_flat_yml(rr):
    result = stylish(generate_diff(
        'tests/fixtures/file1.yml',
        'tests/fixtures/file2.yml')
    )
    assert rr == result


@pytest.fixture
def right_result_nestedyml():
    with open(right_result_nestedYML_path) as right_result_file:
        result_lines = right_result_file.readlines()
    return "".join(result_lines)


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
    result = stylish(generate_diff(
        'tests/fixtures/file1.json',
        'tests/fixtures/file2.json')
    )
    assert right_result == result


def test_yml(right_result):
    result = stylish(generate_diff(
        'tests/fixtures/file1.yml',
        'tests/fixtures/file2.yml')
    )
    assert right_result == result


def test_nested_xml(right_result_nested):
    result = stylish(generate_diff('tests/fixtures/file1_nested.json',
                                   'tests/fixtures/file2_nested.json'))
    assert right_result_nested == result


def test_nested_yml(right_result_nestedyml):
    result = stylish(generate_diff('tests/fixtures/file1_nested.yml',
                                   'tests/fixtures/file2_nested.yml'))
    assert right_result_nestedyml == result
