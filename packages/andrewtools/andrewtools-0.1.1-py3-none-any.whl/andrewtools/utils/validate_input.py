"""Collection of functions used to validate function arguments"""


def validate_type(param_val: any, expected_type: type) -> int:
    """
    Check type of value by attempting to convert to expected type.
    Return converted type, if successful.
    """
    try:
        param_val = expected_type(param_val)
        return param_val
    except (ValueError, TypeError):
        raise
