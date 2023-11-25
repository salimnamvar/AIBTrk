"""
Data Type Check Utilities

This module provides utility functions for checking the data type of values.

Classes:
    None

Functions:
    - `is_float(value: Any) -> bool`: Check if the given value is a floating-point number.
    - `is_int(value: Any) -> bool`: Check if the given value is an integer.
    - `are_uuids(obj: Any) -> bool`: Check if an object is a List[uuid.UUID].

Variables:
    None
"""


# region Import Dependencies
import uuid
from typing import Any
import numpy as np
# endregion Import Dependencies


def is_float(a_obj: Any) -> bool:
    """
    Check if the given value is a floating-point number.

    Args:
        a_obj (Any): The object to be checked.

    Returns:
        bool: True if the value is a floating-point number, False otherwise.
    """
    return isinstance(
        a_obj,
        (
            float,
            np.float_,
            np.float16,
            np.float32,
            np.float64,
        ),
    )


def is_int(a_obj: Any) -> bool:
    """
    Check if the given value is an integer.

    Args:
        a_obj (Any): The object to be checked.

    Returns:
        bool: True if the value is an integer, False otherwise.
    """
    return isinstance(
        a_obj,
        (
            int,
            np.int_,
            np.intc,
            np.intp,
            np.int8,
            np.int16,
            np.int32,
            np.int64,
        ),
    )


def are_uuids(a_obj: Any) -> bool:
    """
    Check if an object is a List[uuid.UUID].

    Args:
        a_obj (Any): The object to check.

    Returns:
        bool: True if the object is a List[uuid.UUID], False otherwise.
    """
    check = False
    # Check if obj is a list/tuple
    if isinstance(a_obj, (list, tuple)):
        # Check if all elements in the list are instances of uuid.UUID
        check = all(isinstance(item, uuid.UUID) for item in a_obj)
    return check
