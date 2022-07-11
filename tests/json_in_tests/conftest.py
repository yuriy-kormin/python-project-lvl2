import pytest
import os

JSON_IN_DIR = 'json_in'


@pytest.fixture
def get_result(fixtures_path, input_file_names, output_files, request):
    result = {}
    workdir = os.path.join(fixtures_path, JSON_IN_DIR, request.param['file_type'])
    result['paths'] = [os.path.join(workdir, i) for i in input_file_names['json']]
    result['formatter'] = request.param['formatter']
    if request.param['reverse'] or 'reverse' not in request.param.keys():
        result['paths'].reverse()
    right_result = output_files[1] if request.param['reverse'] else output_files[0]
    result['result'] = file_content(os.path.join(workdir, request.param['formatter'],right_result))
    return result


def file_content(path):
    with open(path) as file_:
        lines = file_.readlines()
    return "".join(lines)
