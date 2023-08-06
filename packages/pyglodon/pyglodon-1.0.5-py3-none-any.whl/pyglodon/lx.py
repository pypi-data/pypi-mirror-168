# -*- coding: utf-8 -*-


def _get_zi_index(zi, text):
    res = []
    index = text.find(zi)
    while index != -1:
        res.append(index)
        text = text.replace(zi, "*", 1)
        index = text.find(zi)
    return res


def solve_index_drift(original_text, processed_text, processed_listitem_index: list):
    original_listitem_index = []
    for listitem, index in processed_listitem_index:
        zi = listitem[0]
        zi_index_processed_text = _get_zi_index(zi, processed_text)
        if index in zi_index_processed_text:
            zi_relative_position = zi_index_processed_text.index(index)
            # print(zi_relative_position)
            zi_index_original_text = _get_zi_index(zi, original_text)
            original_index = zi_index_original_text[zi_relative_position]
            original_listitem_index.append([listitem, original_index])
        else:
            original_listitem_index([listitem, -1]) 
        
    return original_listitem_index




if __name__ == "__main__":
    original_text = "a s d f g r"
    processed_text = "sdfg"
    processed_listitem_index = [("s", 0), ("d", 1), ("f", 2)]
    res = solve_index_drift(original_text, processed_text, processed_listitem_index)
    print(res)
