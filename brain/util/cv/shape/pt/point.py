""" Point Module

This module provides classes for representing 2D points and a container class for a collection of such points.

Classes:
    - `Point2D`: Represents a 2D point with x and y coordinates.
    - `Point2DList`: Container class for a collection of `Point2D` objects.

Functions:
    None

Variables:
    None
"""


# region Import Dependencies
from typing import Union, List
import numpy as np
from brain.util import BaseObject, is_int, is_float, BaseList

# endregion Import Dependencies


class Point2D(BaseObject):
    """Point2D

    This class represents a 2D point with x and y coordinates.

    Attributes:
        x (Union[int, float]):
            The x-coordinate of the point.
        y (Union[int, float]):
            The y-coordinate of the point.
    """

    def __init__(self, a_x: Union[int, float], a_y: Union[int, float], a_name: str = "POINT") -> None:
        """Constructor for Point2D

        Args:
            a_x (Union[int, float]):
                The x-coordinate value.
            a_y (Union[int, float]):
                The y-coordinate value.
            a_name (str, optional):
                A string specifying the name of the point (default is 'POINT').

        Raises:
            TypeError: If x and y values have different data types.
        """
        super().__init__(a_name)
        if type(a_x) != type(a_y):
            raise TypeError("X and Y values should both have the same data type")
        self.x = a_x
        self.y = a_y

    @property
    def x(self) -> Union[int, float]:
        """X Getter

        Returns:
            Union[int, float]: The x-coordinate of the point.
        """
        return self._x

    @x.setter
    def x(self, a_x: Union[int, float]) -> None:
        """X Setter

        Args:
            a_x (Union[int, float]):
                The new x-coordinate value.

        Raises:
            TypeError: If the provided x-coordinate is not an int or float.
        """
        int_flag = is_int(a_x)
        float_flag = is_float(a_x)
        if a_x is None and not (int_flag or float_flag):
            raise TypeError("The `a_x` should be a int or float.")
        if int_flag:
            a_x = int(a_x)
        if float_flag:
            a_x = float(a_x)
        self._x = a_x

    @property
    def y(self) -> Union[int, float]:
        """Y Getter

        Returns:
            Union[int, float]: The y-coordinate of the point.
        """
        return self._y

    @y.setter
    def y(self, a_y: Union[int, float]) -> None:
        """Y Setter

        Args:
            a_y (Union[int, float]):
                The new y-coordinate value.

        Raises:
            TypeError: If the provided y-coordinate is not an int or float.
        """
        int_flag = is_int(a_y)
        float_flag = is_float(a_y)
        if a_y is None and not (int_flag or float_flag):
            raise TypeError("The `a_y` should be a int or float.")
        if int_flag:
            a_y = int(a_y)
        if float_flag:
            a_y = float(a_y)
        self._y = a_y

    def to_dict(self) -> dict:
        """Convert to Dictionary

        Returns:
            dict: A dictionary representation of the point.
        """
        dic = {"x": self.x, "y": self.y}
        return dic

    def to_tuple(self) -> tuple:
        """Convert to Tuple

        Returns:
            tuple: A tuple representation of the point.
        """
        point = (self._x, self._y)
        return tuple(point)

    def to_list(self) -> list:
        """Convert to List

        Returns:
            list: A list representation of the point.
        """
        point = [self._x, self._y]
        return point

    def to_numpy(self) -> np.ndarray:
        """Convert to NumPy Array

        Returns:
            np.ndarray: A NumPy array representation of the point.
        """
        point = np.asarray(self.to_list())
        return point

    def to_int(self):
        """Converts the coordinates of the point to integers.

        This method modifies the `x` and `y` coordinates of the Point2D instance, rounding them to the nearest integer.
        """
        self._x = int(self._x)
        self._y = int(self._y)

    def to_float(self):
        """Converts the coordinates of the point to floats.

        This method modifies the `x` and `y` coordinates of the Point2D instance, converting them to floating-point
        numbers.
        """
        self._x = float(self._x)
        self._y = float(self._y)

    def __eq__(self, a_point2d: "Point2D") -> bool:
        """Check if two Point2D instances are equal.

        Args:
            a_point2d (Point2D): The Point2D instance to compare.

        Returns:
            bool: True if the coordinates of both Point2D instances are equal, False otherwise.

        Raises:
            TypeError: If `a_point2d` is not an instance of Point2D.
        """
        if a_point2d is None and not isinstance(a_point2d, Point2D):
            raise TypeError("The `a_point2d` should be a `Point2D`.")
        is_equal = self.x == a_point2d.x and self.y == a_point2d.y
        return is_equal

    def __iter__(self):
        """Iterator for the Point object.

        Yields:
            Union[int, float]: The x and y values in sequence.
        """
        yield self.x
        yield self.y

    def __getitem__(self, index):
        """Get an element from the Point object by index.

        Args:
            index (int): The index of the element to retrieve.

        Returns:
            Union[int, float]: The value at the specified index.

        Raises:
            IndexError: If the index is out of range for the Point object.
        """
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range for Point object")

    def speed(self, a_point2d: "Point2D") -> tuple[float, float]:
        """Calculates the normalized speed vector from the current point to another point.

        Args:
            a_point2d (Point2D): The target point to calculate the speed vector towards.

        Returns:
            tuple[float, float]: A tuple representing the normalized speed vector (speed_x, speed_y).

        Raises:
            TypeError: If `a_point` is None or not an instance of Point2D.
        """
        if a_point2d is None or not isinstance(a_point2d, Point2D):
            raise TypeError("The `a_point` should be a `Point2D`.")

        # Calculate the displacement vector between points
        speed = np.array([a_point2d.y - self.y, a_point2d.x - self.x])

        # Calculate the norm (magnitude) of the displacement vector
        norm = np.sqrt((a_point2d.y - self.y) ** 2 + (a_point2d.x - self.x) ** 2) + 1e-10

        # Normalize the speed vector
        normalized_speed = speed / norm

        # Extract components of the normalized speed vector
        speed_x = float(normalized_speed[0])
        speed_y = float(normalized_speed[1])
        return speed_x, speed_y


class Point2DList(BaseList[Point2D]):
    """Point2D List

    The Point2DList class is based on the :class:`ObjectList` class and serves as a container for a collection of
    :class:`Point2D` objects.
    """

    def __init__(self, a_name: str = "Point2DList", a_max_size: int = -1, a_items: List[Point2D] = None):
        super().__init__(a_name=a_name, a_max_size=a_max_size, a_items=a_items)
