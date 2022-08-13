from gendiff import generate_diff
import pytest
import re


def test_unsupported_file_format(input_paths):
    with pytest.raises(Exception) as e:
        generate_diff(input_paths[0], input_paths[1])
    assert re.search('^Unsupported file format', str(e.value))
