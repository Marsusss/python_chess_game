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


def get_nonzero_indices_of_2d_list(input_list):
    """
    This function returns the indices of the non-zero elements in a 2D list.

    The function iterates over the rows and columns of the 2D list. If the element at
    a given row and column is non-zero, the function appends the row and column indices
    to the output list.

    :param input_list: The input 2D list.
    :return: A list of tuples, where each tuple contains the row and column indices of
    a non-zero element in the input list.
    """
    return [
        (i, j)
        for i, row in enumerate(input_list)
        for j, element in enumerate(row)
        if element != 0
    ]


def slice_to_range(s, length):
    return range(*s.indices(length))


def slice_to_list(s, length):
    return list(slice_to_range(s, length))


def is_non_negative(number):
    return number >= 0


def is_non_negative_int(integer):
    result = isinstance(integer, int)
    result &= is_non_negative(integer)
    return result


def is_iterable(iterable):
    try:
        iter(iterable)
    except TypeError:
        return False

    return True


def is_iterable_of_length(
    iterable, iterable_type, required_length=None, min_length=None, max_length=None
):
    if not is_iterable(iterable):
        return False

    result = isinstance(iterable, iterable_type)

    if required_length is not None:
        result &= len(iterable) == required_length

    else:
        if min_length is not None:
            result &= len(iterable) >= min_length

        if max_length is not None:
            result &= len(iterable) <= max_length

    return result


def is_2d_coordinate(coordinate, max_coordinates=None):
    result = is_iterable_of_length(coordinate, tuple, 2)
    for i, dimension in enumerate(coordinate):
        result &= is_non_negative_int(dimension)
        if max_coordinates is not None:
            result &= dimension < max_coordinates[i]

    return result
