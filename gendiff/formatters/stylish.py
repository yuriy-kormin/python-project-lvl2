from gendiff.inner_format import status, get_children,is_dir,get_value,get_old_record
from gendiff.statuses import statuses

indents = {
    statuses['+']: '  + ',
    statuses['-']: '  - ',
    statuses['=']: '    '
}


def make_string(data, name, indent):
    cur_value = get_value(data)
    if cur_value:
        return indent + indents[status(data)] + name + ': ' + get_value(data)
    return None

def make_format(data, name='', indent =''):
    print(data)
# def inner(data, name='', indent=''):
    #сюда даются данные и уже inner решает - это просто запись и надо вернуть value или это словарь с детями
    # print ("---")
    # print(data)
    if is_dir(data):
        result = ['{' if not name else indent + name + ': {']
        children = get_children(data)
        for child in children:
            result.append(make_format(children[child], child,  indent))
        result.append(indent+'}')
    else:
        #это просто запись
        return make_string(data, name, indent+indents[statuses['=']])
    return result
    #
        # cur_value = get_value(data)
        # if cur_value:
        #     return cur_value
        # result = ['{' if not name else indent + name + ': {']
        # for record in data:
        #     cur_status = status(data[record])
        #     cur_value = get_value(data[record])
        #     # cur_children = get_children(data[record])
        #     if cur_status in indents:
        #         result.append(indents[cur_status]+str(record)+ ': '+ inner(data[record]))
        #     else:
        #         # for cur_status in (statuses['-'], statuses['+']):
        #         result.append(indents[statuses['-']]+str(record)+ ': '+ get_value(get_old_record(data[record])))
        #         result.append(indents[statuses['+']] + str(record) + ': ' + get_value(data[record]))
        # result.append(indent+'}')
        # return result
    return "\n".join(inner(data))


def normalize_output(data):
    print("normalize :",data)
    answer = ''
    if type(data) is bool:
        answer = str(data).lower()
    elif data is None:
        answer = 'null'
    else:
        answer = str(data)
    return answer if len(answer) else ''

#
# def is_change_type_to(data):
#     keys = data.keys()
#     if 'change_type_to' in keys:
#         return data['change_type_to']
#     return None
#
#
# def make_string(dict_, closed_line=False, mark=True):
#     result = []
#     level = len(dict_['path']) - 1
#     if closed_line:
#         result.append(stylish_indents[statuses['=']] * level + '}')
#     else:
#         if dict_['diff'] == statuses['!=']:
#             for diff_key in (statuses['-'], statuses['+']):
#                 dict_['diff'] = diff_key
#                 if not is_change_type_to(dict_):
#                     if diff_key == statuses['-']:
#                         dict_['value'] = dict_['old_value']
#                     else:
#                         dict_['value'] = dict_['new_value']
#                 result.extend(make_string(dict_, False, mark))
#         else:
#             value = '{' if is_dir(False, dict_) else dict_['value']
#             spaces = stylish_indents[dict_['diff']] if mark \
#                 else stylish_indents[statuses['=']]
#             string_begin = stylish_indents[statuses['=']] * level \
#                 + spaces + dict_['name'] + ":" + make_out_format(value)
#             result.append(string_begin)
#     return result
#
#
# def make_format(data):
#     def inner(id, data, mark=True):
#         mark_status = mark
#         result = []
#         result.append('{') if id == 0 else None
#         records = get_records_in_branch(id, data, sort_by_name=True)
#         for child in records:
#             if is_change_type_to(records[child]) == 'dir':
#                 records[child]['value'] = records[child]['old_value']
#                 records[child]['diff'] = statuses['-']
#                 result.extend(make_string(records[child], mark=mark_status))
#                 records[child].pop('value')
#                 records[child]['children'] = records[child]['new_children']
#                 records[child]['diff'] = statuses['+']
#                 result.extend(make_string(records[child], mark=mark_status))
#                 mark_status = False
#                 result.extend(inner(child, data, mark=mark_status))
#                 records[child].pop('children')
#                 mark_status = mark
#             elif is_change_type_to(records[child]) == 'value':
#                 records[child]['children'] = records[child]['old_children']
#                 records[child]['diff'] = statuses['-']
#                 result.extend(make_string(records[child], mark=mark_status))
#                 mark_status = False
#                 result.extend(inner(child, data, mark=mark_status))
#                 mark_status = mark
#                 records[child].pop('children')
#                 records[child]['value'] = records[child]['new_value']
#                 records[child]['diff'] = statuses['+']
#                 result.extend(make_string(records[child], mark=mark_status))
#                 records[child].pop('value')
#                 mark_status = mark
#             else:
#                 result.extend(make_string(records[child], mark=mark_status))
#             if is_dir(False, records[child]):
#                 if records[child]['diff'] != statuses['=']:
#                     mark_status = False
#                 result.extend(inner(child, data, mark=mark_status))
#                 mark_status = mark
#         result.extend(
#             make_string(records[child], closed_line=True, mark=mark_status))
#         return result
#
#     res = inner(0, data)
#     return "\n".join(res)
