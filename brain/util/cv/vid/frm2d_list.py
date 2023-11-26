""" 2D Frame List

    This Python file contains the definition of the :class:`Frame2DList` class, which serves as a container for a
    collection of 2D frame objects (:class:`Frame2D`).

Classes:
    `Frame2DList`:
        The `Frame2DList` class is based on the :class:`ObjectList` class and serves as a container for a
        collection of :class:`Frame2D` objects.
Functions:
    None
Variables:
    None
"""

# region Imported Dependencies
from typing import List
from brain.util import BaseList, Frame2D
# endregion Imported Dependencies


class Frame2DList(BaseList[Frame2D]):
    """Frame2D List

    The Frame2D List class is based on the :class:`ObjectList` class and serves as a container for a collection of
    :class:`Frame2D` objects.
    """

    def __init__(self, a_name: str = "Frame2DList", a_max_size: int = -1, a_items: List[Frame2D] = None):
        super().__init__(a_name=a_name, a_max_size=a_max_size, a_items=a_items)
