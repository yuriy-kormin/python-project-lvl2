import pytest
from gendiff import generate_diff
import json


@pytest.mark.parametrize(
    'get_yaml_inputs', ('empty', 'flat', 'nested'), indirect=True)
def test_one(get_yaml_inputs):
    diff = generate_diff(get_yaml_inputs[0], get_yaml_inputs[1], 'json')
    assert isinstance(json.loads(diff), dict)
