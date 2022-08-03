from gendiff.formatters.stylish import make_format as make_stylish
from gendiff.formatters.plain import make_format as make_plain
from gendiff.formatters.json import make_format as make_json

FORMATS = {'stylish': make_stylish,
           'plain': make_plain,
           'json': make_json}
