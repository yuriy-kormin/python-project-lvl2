import pytest
from gendiff import generate_diff


@pytest.mark.parametrize('get_result', ({"file_type": 'empty', "formatter": 'stylish'},
                                        {"file_type": 'empty', "formatter": 'stylish', 'reverse': True},
                                        {"file_type": 'empty', "formatter": 'plain'},
                                        {"file_type": 'empty', "formatter": 'plain', 'reverse': True},
                                        {"file_type": 'empty', "formatter": 'json'},
                                        {"file_type": 'empty', "formatter": 'json', 'reverse': True}
                                        ), indirect=True)
def test_empty(get_result):
    assert get_result['result'] == generate_diff(get_result['paths'][0], get_result['paths'][1], get_result['formatter'])
