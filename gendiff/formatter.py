from gendiff.formatters.stylish import render_stylish
from gendiff.formatters.plain import render_plain
from gendiff.formatters.json import render_json

FORMATS = {'stylish': render_stylish,
           'plain': render_plain,
           'json': render_json}


def formatting(format_name):
    if format_name in FORMATS:
        return FORMATS[format_name]
    raise ValueError(f"Unsupported output format: {format_name}")


def get_formats():
    return FORMATS.keys()
