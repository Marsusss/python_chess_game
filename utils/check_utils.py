import utils.utils as utils


def check_is_instance(var_name, var, var_type):
    if not isinstance(var, var_type):
        raise TypeError(
            f"{var_name} must be a {var_type.__name__}, got {type(var).__name__}"
        )


def check_is_instance_of_types(var_name, var, var_types):
    for var_type in var_types:
        if isinstance(var, var_type):
            break
    else:
        raise TypeError(
            f"{var_name} must be an instance of any of the following types: "
            f"{', '.join([var_type.__name__ for var_type in var_types])}, but got "
            f"{type(var).__name__}."
        )


def check_is_non_negative(number_name, number):
    if not utils.is_non_negative(number):
        raise ValueError(
            f"{number_name} must be greater than or equal to 0, got {number}"
        )


def check_is_non_negative_int(integer_name, integer):
    check_is_instance(integer_name, integer, int)
    check_is_non_negative(integer_name, integer)


def check_is_index(index, element_count):
    if not isinstance(index, slice):
        check_is_instance("index", index, int)
        if index >= element_count:
            raise IndexError(
                f"index must be less than the number of entries"
                f"({element_count}), got {index}"
            )
    else:
        if index.stop > element_count:
            raise IndexError(
                f"index must be less than the number of entries"
                f"({element_count}), but got max of slice {index.stop}"
            )


def check_is_iterable(iterable_name, iterable):
    if not utils.is_iterable(iterable):
        raise TypeError(
            f"Expected {iterable_name} to be an iterable, but got" f"{type(iterable)}"
        )


def check_is_iterable_of_length(
    iterable_name,
    iterable,
    iterable_type,
    required_length=None,
    min_length=None,
    max_length=None,
):
    check_is_iterable(iterable_name, iterable)
    check_is_instance(iterable_name, iterable, iterable_type)
    if required_length is not None:
        if len(iterable) != required_length:
            raise ValueError(
                f"Error: {iterable_name} has length {len(iterable)}, "
                f"expected length == {required_length}."
            )

    else:
        if min_length is not None:
            if len(iterable) < min_length:
                raise ValueError(
                    f"Error: {iterable_name} has length {len(iterable)}, "
                    f"expected length > {min_length}."
                )

        if max_length is not None:
            if len(iterable) > max_length:
                raise ValueError(
                    f"Error: {iterable_name} has length {len(iterable)}, "
                    f"expected length < {max_length}."
                )


def check_elements_are_unique(iterable_name, iterable):
    if len(iterable) != len(set(iterable)):
        raise ValueError(
            f"Error: Expected {iterable_name} to have unique elements, but got "
            f"only {len(set(iterable))} unique of {len(iterable)} elements."
        )


def check_is_iterable_of_unique_elements(iterable_name, iterable, iterable_type):
    check_is_instance(iterable_name, iterable, iterable_type)
    check_elements_are_unique(iterable_name, iterable)


def check_is_iterable_of_unique_elements_with_length(
    iterable_name,
    iterable,
    iterable_type,
    required_length=None,
    min_length=None,
    max_length=None,
):
    check_is_iterable_of_length(
        iterable_name, iterable, iterable_type, required_length, min_length, max_length
    )
    check_elements_are_unique(iterable_name, iterable)


def check_is_2d_coordinate(coordinate, max_coordinates=None):
    check_is_iterable_of_length("2D_coordinate", coordinate, tuple, 2)
    for i, dimension in enumerate(coordinate):
        check_is_non_negative_int(f"2D_coordinate[{i}]", dimension)
        if max_coordinates is not None:
            if dimension >= max_coordinates[i]:
                raise ValueError(
                    f"coordinate {coordinate} is out of bounds for max "
                    f"{max_coordinates}"
                )
