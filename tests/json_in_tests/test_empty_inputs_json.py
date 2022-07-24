import pytest
from gendiff import generate_diff
import json


@pytest.mark.parametrize('get_result', (
        {"file_type": 'empty', "formatter": 'stylish'},
        {"file_type": 'empty', "formatter": 'stylish','reverse': True},
        {"file_type": 'empty', "formatter": 'plain'},
        {"file_type": 'empty', "formatter": 'plain','reverse': True}
                                        ), indirect=True)
def test_empty_jsons(get_result):
    assert get_result['result'] == generate_diff(get_result['paths'][0],
                                                 get_result['paths'][1],
                                                 get_result['formatter'])

#
# @pytest.mark.json
# @pytest.mark.parametrize('get_inputs', ['empty'], indirect=True)
# def test_json_output(get_inputs):
#     # print(generate_diff(get_inputs[0], get_inputs[1], 'json'))
#     assert isinstance(generate_diff(get_inputs[0], get_inputs[1], 'json'), dict)
