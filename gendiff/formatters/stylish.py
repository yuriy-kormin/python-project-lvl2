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


def make_string(data, level, first=False, last=False):
    print('make string    data=', data, '\nlevel=', level)
    if first:
        print('make first string')
        if not is_record(data) and not is_dir(data):
            # its mean, that this property is root
            return "{"
        elif is_dir(data):
            return get_indent(data,level-1) + get_name(data) + ': {'
    if last:
        return get_indent(data, level, last=True) + '}'
    value = normalize_output(get_value(data))
    name = get_name(data)
    return get_indent(data,level) + name + ': ' + value


def get_indent(property, level, last=False):
    if last:
        return (level) * indents['']
    print('get indent to ', property)
    cur_status = get_status(property)
    print('get_status is \'' + cur_status + '\'')
    cur_indent = level * indents['']
    if cur_status in indents:
        return cur_indent + indents[cur_status]
    return cur_indent + '$$$$'


def make_format(data, level=-1):
    children = get_children(data, sorted_=True)
    level += 1
    if len(children) > 0:
        result = [make_string(data,level, first=True)]
        for child in children:
            print('working with child', get_name(child))
            print('result is ', result)
            if is_record(child):
                result.append(make_string(child, level))
            else:
                result.append(make_format(child, level))
        result.append(make_string(data,level, last=True))
    else:
        result = ['{', '}']
    print ('result is ', result)
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
