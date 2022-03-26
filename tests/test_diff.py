import pytest
from gendiff import generate_diff
from tests.fixtures.output import right_result

# @pytest.mark.usefixtures
def test_step4(right_result):
    # print(right_result())
    result = generate_diff('tests/fixtures/file1.json','tests/fixtures/file2.json')
    assert right_result == result