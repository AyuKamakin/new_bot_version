def merge_lists_from_dict(dictionary):
    merged_list = []
    for sublist in dictionary.values():
        merged_list.extend(sublist)
    return merged_list


def get_num_from_name(string: str, dictionary: dict):
    list_united = merge_lists_from_dict(dictionary)
    if string in list_united:
        return list_united.index(string)
    else:
        return None


def get_name_from_num(number: int, dictionary: dict):
    list_united = merge_lists_from_dict(dictionary)
    if int(number) < int(len(list_united)):
        return list_united[int(number)]
    else:
        return None


def get_cat_from_num(number: int, dictionary: dict):
    if int(number) < int(len(list(dictionary.keys()))):
        return list(dictionary.keys())[int(number)]
    else:
        return None


def get_num_from_cat(string: str, dictionary: dict):
    if string in list(dictionary.keys()):
        return list(dictionary.keys()).index(string)
    else:
        return None
