# pylint: disable=missing-docstring

def find_item(item, item_list):
    for i, other in enumerate(item_list):
        if other == item:
            break
    return i
