from gendiff.inner_format import get_status, get_name, get_children, is_record, is_dir, get_value, set_value, \
    get_old_record, \
    set_status, set_children
from gendiff.statuses import statuses

indents = {
    statuses['+']: '  + ',
    statuses['-']: '  - ',
    statuses['=']: '    ',
    '': ''
}


def make_string(data, indent):
    value = get_value(data)
    name = get_name(data)
    # status = get_status(data) if get_status(data) else ''
    return indent + get_indent(data)[0] + name + ': ' + value
    # return None


def get_indent(property):
    cur_status = get_status(property)
    if cur_status in statuses.values():
        return [indents[cur_status]]
    return [indents[statuses['=']],
            indents[statuses['+']]]


def make_first_string(data, indent):
    print ('make first string to ',data)
    if not is_record(data) and not is_dir(data):
        # its mean, that this property is root
        return "{"
    elif is_dir(data):
        return indent + get_indent(data)[0] + get_name(data) + ': {'


def make_format(data, level = -1):
    indent = level * '    '
    # if data is list - its dir, else record
    # print(sorted(data, key = lambda v: v['name']))
    # print ('make format to ',data)
    if is_record(data):
        return make_string(data, indent)
    else:
        # this is dir
        children = get_children(data, sorted_=True)
        # status = get_status(data)
        result = [make_first_string(data, indent)]
        for property in children:
            # print(result)
            result.append(make_format(property, level+1))
            # print (result)
        result.append(indent + '}')

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
