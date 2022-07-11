import pytest
import os

FIXTURES_PATH = 'fixtures'
INPUT_JSON_FILE1 = 'file1.json'
INPUT_JSON_FILE2 = 'file2.json'
INPUT_YAML_FILE1 = 'file1.yaml'
INPUT_YAML_FILE2 = 'file2.yaml'
OUTPUT = 'output'
OUTPUT_REVERSED = 'output_r'
FORMATTERS = ('stylish', 'plain')

@pytest.fixture
def fixtures_path():
    return os.path.join(os.path.dirname(__file__), FIXTURES_PATH)


@pytest.fixture
def input_file_names():
    return {
        'json': (INPUT_JSON_FILE1, INPUT_JSON_FILE2),
        'yaml': (INPUT_YAML_FILE1, INPUT_YAML_FILE2)
    }


@pytest.fixture
def output_files():
    return OUTPUT, OUTPUT_REVERSED


@pytest.fixture
def formatters():
    return FORMATTERS
