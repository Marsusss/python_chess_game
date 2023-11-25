def check_is_instance(var_name, var, var_type):
    if not isinstance(var, var_type):
        raise TypeError(
            f"{var_name} must be a {var_type.__name__}, got {type(var).__name__}"
        )


def check_is_positive(number_name, number):
    if number < 0:
        raise ValueError(
            f"{number_name} must be greater than or equal to 0, got {number}"
        )


def check_is_positive_int(integer_name, integer):
    check_is_instance(integer_name, integer, int)
    check_is_positive(integer_name, integer)


def check_is_index(index, element_count):
    check_is_positive_int("index", index)
    if index >= element_count:
        raise IndexError(
            f"index must be less than the number of entries"
            f"({element_count}), got {index}"
        )
