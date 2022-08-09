def render_stylish(tree):
    return _node_processing(tree)


def _build_indent(level, status=None):
    result = level * '    '
    if status:
        if status == 'added':
            return result + '  + '
        if status == 'removed':
            return result + '  - '
        if status == 'equals':
            return result + '    '
    return result


def _node_processing(node, level=0):
    name = node.get('key')
    children = node.get('children')
    node_type = node.get('type')
    formatted_value = _process_value(node.get('value'), level)
    formatted_value1 = _process_value(node.get('old_value'), level)
    formatted_value2 = _process_value(node.get('new_value'), level)
    indent = _build_indent(level, node_type)
    if node_type == 'root':
        lines = map(lambda child: _node_processing(child, level), children)
        result = '\n'.join(lines)
        return f'{{\n{result}\n}}'
    elif node_type == 'nested':
        lines = map(lambda child: _node_processing(child, level + 1), children)
        result = '\n'.join(lines)
        return f"{indent}    {name}: {{\n{result}\n{indent}    }}"
    elif node_type == 'updated':
        result = [
            _build_indent(level, 'removed') + f'{name}: {formatted_value1}',
            _build_indent(level, 'added') + f'{name}: {formatted_value2}']
        return '\n'.join(result)
    # if node_type in ('added', 'removed', 'equals'):
    return _build_indent(level, node_type) + name + ': ' + formatted_value


def _process_value(data, level):
    if isinstance(data, dict):
        result = ''
        indent = _build_indent(level, 'equals')
        for record in data:
            value = _process_value(data[record], level + 1)
            result += f'\n{indent}    {record}: {value}'
        return f'{{{result}\n{indent}}}'
    else:
        return _to_str(data)


def _to_str(data):
    if isinstance(data, bool):
        return str(data).lower()
    elif data is None:
        return 'null'
    return str(data)
