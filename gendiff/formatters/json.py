import json


def render_json(data):
    return json.dumps(data, indent=4)
