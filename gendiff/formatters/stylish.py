from gendiff.inner_format import get_status, get_name, get_children, \
    is_record, is_dir, get_value, get_old_record
from gendiff.statuses import statuses

indents = {
    statuses['+']: '  + ',
    statuses['-']: '  - ',
    statuses['=']: '    ',
    '': '    '
}


def make_string(data, level, first=False, last=False):
    if first:
        if not is_record(data) and not is_dir(data):
            # its mean, that this property is root
            return "{"
        elif is_dir(data):
            return get_indent(data, level - 1) + get_name(data) + ': {'
    if last:
        return get_indent(data, level, last) + '}'
    value = normalize_output(get_value(data))
    name = get_name(data)
    return get_indent(data, level) + name + ': ' + value


def get_indent(property, level, last=False):
    if last:
        return level * indents['']
    cur_status = get_status(property)
    cur_indent = level * indents['']
    if cur_status in indents:
        return cur_indent + indents[cur_status]
    # this block executes, if value was updated
    # result = []
    old_record = [get_old_record(property)]
    # tmp =
    result = [make_format(old_record, level-1)]
    result.append(cur_indent + indents[statuses['+']])
    return "\n".join(result)


def make_format(data='', level=-1):
    # print ("\nnew make_format\n", data, level)
    children = get_children(data, sorted_=True)
    level += 1
    if len(children) > 0:
        result = [make_string(data, level, first=True)]
        for child in children:
            if is_record(child):
                result.append(make_string(child, level))
            else:
                result.append(make_format(child, level))
        result.append(make_string(data, level, last=True))
    else:
        result = ['{', '}']
        # return result
    # result = inner (data,level)
    # print('result is ', result)
    return "\n".join(result)


def normalize_output(data):
    # print("normalize :", data)
    answer = ''
    if type(data) is bool:
        answer = str(data).lower()
    elif data is None:
        answer = 'null'
    else:
        answer = str(data)
    return answer if len(answer) else ''
