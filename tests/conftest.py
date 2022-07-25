import pytest
import os

JSON_IN_DIR = 'json_in'
YAML_IN_DIR = 'yaml_in'
FIXTURES_PATH = 'fixtures'
INPUT_JSON_FILE1 = 'file1.json'
INPUT_JSON_FILE2 = 'file2.json'
INPUT_YAML_FILE1 = 'file1.yml'
INPUT_YAML_FILE2 = 'file2.yml'
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


@pytest.fixture
def json_in():
    return JSON_IN_DIR


@pytest.fixture
def yaml_in():
    return YAML_IN_DIR


@pytest.fixture
def get_json_inputs(fixtures_path, input_file_names, json_in, request):
    workdir = os.path.join(fixtures_path, json_in, request.param)
    return [os.path.join(workdir, i) for i in input_file_names['json']]
