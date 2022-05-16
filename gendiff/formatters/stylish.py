from gendiff.inner_format import get_status, get_name, get_children, \
    is_record, is_dir, get_value, set_value, get_old_record, \
    set_status, set_children
from gendiff.statuses import statuses

indents = {
    statuses['+']: '  + ',
    statuses['-']: '  - ',
    statuses['=']: '    ',
    '': '    '
}


def make_string(data='', indent='', first=False, last=False):
    print('make string    data=', data, '\nindent=', indent, '|')
    if first:
        print('make first string')
        if not is_record(data) and not is_dir(data):
            # its mean, that this property is root
            return "{"
        elif is_dir(data):
            return indent + get_name(data) + ': {'
    if last:
        return indent + '}'
    value = get_value(data)
    name = get_name(data)
    return indent + name + ': ' + value


def get_indent(property, level):
    print('get indent to ', property)
    cur_status = get_status(property)
    print('get_status is \'' + cur_status + '\'')
    cur_indent = level * '    '
    if cur_status in indents:
        return cur_indent + indents[cur_status]
    return cur_indent + '$$$$'


def make_format(data, level=-1):
    children = get_children(data, sorted_=True)
    if len(children) > 0:
        result = [make_string(data, get_indent(data, level), first=True)]
        for child in children:
            print('working with child', get_name(child))
            if is_record(child):
                result.append(make_string(child, get_indent(child, level+1)))
            else:
                result.append(make_format(child, level+1))
        result.append(make_string(data, (level+1)*"    ", last=True))
    else:
        result = ['{', '}']
    return "\n".join(result)


def normalize_output(data):
    print("normalize :", data)
    answer = ''
    if type(data) is bool:
        answer = str(data).lower()
    elif data is None:
        answer = 'null'
    else:
        answer = str(data)
    return answer if len(answer) else ''
