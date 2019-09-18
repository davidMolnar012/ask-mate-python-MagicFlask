from collections import OrderedDict


def dict_sort(nested_dict):
    temp_dict = OrderedDict([])
    list_of_dict = [*nested_dict.values()]
    list_of_dict = sorted(list_of_dict, key=lambda x: x['submission_time'], reverse=True)
    for index, item in enumerate(list_of_dict):
        temp_dict[item['id']] = item

    return temp_dict

