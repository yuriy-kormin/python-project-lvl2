import pytest
from gendiff import generate_diff
import json
import os


@pytest.mark.parametrize('get_json_inputs', ('empty', 'flat', 'nested')
    , indirect=True)
def test_one(get_json_inputs):
    diff = generate_diff(get_json_inputs[0], get_json_inputs[1], 'json')
    assert isinstance(json.loads(diff), dict)
