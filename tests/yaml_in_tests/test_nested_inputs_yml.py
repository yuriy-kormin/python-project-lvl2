import pytest
from gendiff import generate_diff


@pytest.mark.parametrize('get_result', ({"file_type": 'nested', "formatter": 'stylish'},
                                        {"file_type": 'nested', "formatter": 'stylish',
                                         'reverse': True},
                                        {"file_type": 'nested', "formatter": 'plain'},
                                        {"file_type": 'nested', "formatter": 'plain',
                                         'reverse': True}
                                        ), indirect=True)
def test_nested_yml(get_result):
    assert get_result['result'] == generate_diff(get_result['paths'][0],
                                                 get_result['paths'][1],
                                                 get_result['formatter'])
