from gendiff import generate_diff
import pytest


@pytest.mark.xfail()
def test_unsupported_file_format(input_paths):
    assert generate_diff(input_paths[0], input_paths[1]) == 0
