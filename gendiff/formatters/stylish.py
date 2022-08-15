def render_stylish(tree):
    return _node_processing(tree)


def _build_indent(level):
    indent = ' ' * 4
    return level * indent


def _node_processing(node, level=0):
    name = node.get('key')
    children = node.get('children')
    node_type = node.get('type')
    formatted_value = _to_str(node.get('value'), level)
    formatted_value1 = _to_str(node.get('old_value'), level)
    formatted_value2 = _to_str(node.get('new_value'), level)
    indent = _build_indent(level)
    if node_type == 'root':
        lines = map(lambda child: _node_processing(child, level), children)
        result = '\n'.join(lines)
        return f'{{\n{result}\n}}'
    if node_type == 'nested':
        lines = map(lambda child: _node_processing(child, level + 1), children)
        result = '\n'.join(lines)
        return f"{indent}    {name}: {{\n{result}\n{indent}    }}"
    if node_type == 'updated':
        result = [f'{indent}  - {name}: {formatted_value1}',
                  f'{indent}  + {name}: {formatted_value2}']
        return '\n'.join(result)
    if node_type == 'added':
        return f'{indent}  + {name}: {formatted_value}'
    if node_type == 'removed':
        return f'{indent}  - {name}: {formatted_value}'
    if node_type == 'equals':
        return f'{indent}    {name}: {formatted_value}'
    raise ValueError(f'Unsupported node type: {node_type}')


def _to_str(data, level):
    if isinstance(data, bool):
        return str(data).lower()
    elif data is None:
        return 'null'
    elif isinstance(data, dict):
        result = ''
        indent = _build_indent(level + 1)
        for record in data:
            value = _to_str(data[record], level + 1)
            result += f'\n{indent}    {record}: {value}'
        return f'{{{result}\n{indent}}}'
    return str(data)
