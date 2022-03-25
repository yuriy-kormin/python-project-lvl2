# import pytest
# from gendiff import generate_diff
from .fixtures.output import right_result

def test_step4(right_result):
    print(right_result())
