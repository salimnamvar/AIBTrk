"""2D Image List Module

This Python file contains the definition of the :class:`Image2DList` class, an object class that stores a
collection of :class:`Image2D` objects.

Classes:
    - `Image2DList`: The class serves as a container for a collection of `Image2D` objects.

Functions:
    None

Variables:
    None
"""

# region Imported Dependencies
from typing import List
from brain.util import BaseList
from brain.util.cv.img import Image2D
# endregion Imported Dependencies


class Image2DList(BaseList[Image2D]):
    """Image2D List

    The Image2DList class is based on the :class:`ObjectList` class and serves as a container for a collection of
    :class:`Image2D` objects.
    """

    def __init__(self, a_name: str = "Image2DList", a_max_size: int = -1, a_items: List[Image2D] = None):
        super().__init__(a_name=a_name, a_max_size=a_max_size, a_items=a_items)
