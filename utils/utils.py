def circular_permute_dict_values(input_dict):
    """
    This function takes a dictionary and returns a new dictionary where the values are
    shifted in a circular manner.
    :param input_dict: The input dictionary.
    :return: A new dictionary with the values shifted in a circular manner.
    """
    values = list(input_dict.values())
    values = values[1:] + values[:1]  # This line performs the circular shift
    return {key: value for key, value in zip(input_dict.keys(), values)}


def get_next_list_element(input_list, current_element):
    """
    This function returns the element that follows a given element in a list.

    The function finds the index of the current element in the list. If the current
    element is the last element in the list, the function returns the first element.
    Otherwise, it returns the element that follows the current element.

    :param input_list: The input list.
    :param current_element: The current element.
    :return: The element that follows the current element in the list. If the current
    element is the last element in the list, the function returns the first element.
    """
    current_idx = input_list.index(current_element)
    if current_idx == len(input_list) - 1:
        return input_list[0]

    else:
        return input_list[current_idx + 1]
