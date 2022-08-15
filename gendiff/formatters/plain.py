def render_plain(tree):
    return _node_processing(tree)


def _node_processing(node, path=''):
    property_path = f"{path}{node.get('key')}"
    children = node.get('children')
    node_type = node.get('type')
    formatted_value = _to_str(node.get('value'))
    formatted_value1 = _to_str(node.get('old_value'))
    formatted_value2 = _to_str(node.get('new_value'))
    result = f"Property '{property_path}' was {node_type}"
    if node_type == 'root':
        lines = filter(None, map(
            lambda child: _node_processing(child), children))
        return '\n'.join(lines)
    elif node_type == 'nested':
        lines = filter(None,
                       map(lambda child: _node_processing(
                           child, f"{property_path}."), children))
        return '\n'.join(lines)
    elif node_type == 'added':
        return f"{result} with value: {formatted_value}"
    elif node_type == 'removed':
        return result
    elif node_type == 'updated':
        return f"{result}. From {formatted_value1} to {formatted_value2}"
    elif node_type != 'equals':
        raise ValueError(f'Unsupported node type: {node_type}')


def _to_str(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    elif isinstance(value, int):
        return str(value)
    return f"'{str(value)}'"
