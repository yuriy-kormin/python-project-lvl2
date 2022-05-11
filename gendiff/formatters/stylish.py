from gendiff.inner_format import status, get_children,is_dir,get_value,get_old_record
from gendiff.statuses import statuses

indents = {
    statuses['+']: '  + ',
    statuses['-']: '  - ',
    statuses['=']: '    '
}


def normalize_output(data):
    # print("normalize :",data)
    answer = get_value(data)
    if type(data) is bool:
        answer = str(answer).lower()
    elif data is None:
        answer = 'null'
    else:
        answer = str(answer)
    return answer if len(answer) else ''


def make_string(data, name, indent):
    result = []
    cur_value = normalize_output(data)
    cur_status = status(data)
    if cur_status == statuses['!=']:
        values = {indents[statuses['-']]: normalize_output(get_old_record(data)), indents[statuses['+']]: cur_value}
    else:
        values = {indents[cur_status]: cur_value}
    for cur_status in values:
        result.append(indent + cur_status + name + ': ' + values[cur_status])
    return result


def make_format(data, name='', indent=''):
    print(data)
    #сюда даются данные и уже inner решает - это просто запись и надо вернуть value или это словарь с детями
    # print ("---")
    # print(data)
    if is_dir(data):
        result = ['{' if not name else indent + name + ': {']
        children = get_children(data)
        for child in sorted(children):
            result.extend(make_format(children[child], child,  indent))
        result.append(indent+'}')
    else:
        #это просто запись
        return make_string(data, name, indent)
    # return result
    return "\n".join(result)