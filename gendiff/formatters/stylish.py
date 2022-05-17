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
    if first and is_dir(data):
        return get_indent(data, level) + get_name(data) + ': {'
    if last:
        return get_indent(data, level, last) + '}'
    value = normalize_output(get_value(data))
    value = " "+value if len(value) else value
    name = get_name(data)
    return get_indent(data, level) + name + ':' + value


def get_indent(property, level, last=False):
    if last:
        return level * indents['']
    cur_status = get_status(property)
    cur_indent = level * indents['']
    if cur_status in indents:
        return cur_indent + indents[cur_status]
    # this block executes, if value was updated
    old_record = [get_old_record(property)]
    # result = [make]
    result = make_block(old_record, level-1)
    result.append(cur_indent + indents[statuses['+']])
    # print ('result for updated is ', result)
    return "\n".join(result)


def make_block(data, level):
    # print ("\nnew make_format\n", data, level)
    children = get_children(data, sorted_=True)
    # print('children is ', children)
    level += 1
    result = []
    if len(children) > 0:
        for child in children:
            if is_record(child):
                result.append(make_string(child, level))
            else:
                result.append(make_string(child, level, first=True))
                result.extend(make_block(child, level))
                result.append(make_string(data, level+1, last=True))
    return result


def make_format(data):
    result = ['{']
    result.extend(make_block(data, level=-1))
    result.append('}')
    return "\n".join(result)


def normalize_output(data):
    if type(data) is bool:
        answer = str(data).lower()
    elif data is None:
        answer = 'null'
    else:
        answer = str(data)
    return answer if len(answer) else ''
