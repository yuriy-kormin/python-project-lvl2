import pytest
import os


@pytest.fixture
def input_paths(fixtures_path, unsupported_in, input_file_names):
    workdir = os.path.join(fixtures_path, unsupported_in)
    return [os.path.join(workdir, i) for i in input_file_names['unsupported']]
