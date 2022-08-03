from gendiff.formatters.stylish import render_stylish
from gendiff.formatters.plain import render_plain
from gendiff.formatters.json import render_json

FORMATS = {'stylish': render_stylish,
           'plain': render_plain,
           'json': render_json}
