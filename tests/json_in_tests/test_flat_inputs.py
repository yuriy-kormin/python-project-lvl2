import pytest
from gendiff import generate_diff


@pytest.mark.parametrize('get_result', ({"file_type": 'flat', "formatter": 'stylish'},
                                        {"file_type": 'flat', "formatter": 'stylish', 'reverse': True},
                                        {"file_type": 'flat', "formatter": 'plain'},
                                        {"file_type": 'flat', "formatter": 'plain', 'reverse': True},
                                        {"file_type": 'flat', "formatter": 'json'},
                                        {"file_type": 'flat', "formatter": 'json', 'reverse': True}
                                        ), indirect=True)
def test_flat(get_result):
    assert get_result['result'] == generate_diff(get_result['paths'][0], get_result['paths'][1], get_result['formatter'])
