import pytest
import os


@pytest.fixture
def get_result(fixtures_path, yaml_in, input_file_names, output_files, request):
    result = {}
    workdir = os.path.join(fixtures_path, yaml_in,
                           request.param['file_type'])
    result['paths'] = [
        os.path.join(workdir, i) for i in input_file_names['yaml']
    ]
    result['formatter'] = request.param['formatter']
    if 'reverse' in request.param.keys() and request.param['reverse']:
        result['paths'].reverse()
        right_result = output_files[1]
    else:
        right_result = output_files[0]
    result['result'] = file_content(os.path.join(workdir,
                                                 request.param['formatter'],
                                                 right_result))
    return result


def file_content(path):
    with open(path) as file_:
        lines = file_.readlines()
    return "".join(lines)


@pytest.fixture
def get_yaml_inputs(fixtures_path, input_file_names, yaml_in, request):
    workdir = os.path.join(fixtures_path, yaml_in, request.param)
    return [os.path.join(workdir, i) for i in input_file_names['yaml']]
