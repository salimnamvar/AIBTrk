""" KeyPoint Module

This module provides classes for representing 2D keypoints and a container class for a collection of such keypoints.

Classes:
    - `KeyPoint2D`: Represents a 2D keypoint with x and y coordinates and an optional score.
    - `KeyPoint2DList`: Container class for a collection of `KeyPoint2D` objects.

Functions:
    None

Variables:
    None
"""


# region Import Dependencies
from typing import Union, List, Optional, Tuple
import numpy as np
from brain.util import Point2D, is_float, BaseList

# endregion Import Dependencies


class KeyPoint2D(Point2D):
    def __init__(
        self, a_x: Union[int, float], a_y: Union[int, float], a_score: Optional[float] = None, a_name: str = "KEY_POINT"
    ) -> None:
        # Validate inputs
        x, y, score = self._validate(a_x=a_x, a_y=a_y, a_score=a_score)

        # Initialize keypoint
        super().__init__(a_x=x, a_y=y, a_name=a_name)
        self.score: float = a_score

    def _validate_dtypes(
        self,
        a_x: Union[int, float],
        a_y: Union[int, float],
        a_score: Optional[float] = None,
    ) -> Tuple[int, int, float]:
        # Convert the data types of points to be int
        a_x = int(a_x)
        a_y = int(a_y)

        # Convert score data type to be a float
        if a_score is not None:
            a_score = float(a_score)

        return a_x, a_y, a_score

    def _validate(
        self,
        a_x: Union[int, float],
        a_y: Union[int, float],
        a_score: Optional[float] = None,
    ) -> Tuple[int, int, float]:
        # Correct data types
        x, y, score = self._validate_dtypes(a_x, a_y, a_score)

        # NOTE: The validation process can be expanded based on the use-case
        return x, y, score

    @property
    def score(self) -> float:
        return self._score

    @score.setter
    def score(self, a_score: float = None):
        if a_score is not None:
            float_flag = is_float(a_score)
            if not float_flag:
                raise TypeError("The `a_score` should be a float.")
            if float_flag:
                a_score = float(a_score)
                if a_score > 1.0:
                    a_score = a_score / 100.0
        self._score: float = a_score

    def to_dict(self) -> dict:
        dic = {"x": self.x, "y": self.y, "score": self.score}
        return dic

    @classmethod
    def validate_array(cls, a_coordinates: Union[Tuple, List, np.ndarray]) -> None:
        if a_coordinates is None or not isinstance(a_coordinates, (Tuple, List, np.ndarray)):
            raise TypeError("The `a_coordinates` should be a `Tuple, List, or np.ndarray`.")

        if not isinstance(a_coordinates, np.ndarray):
            a_coordinates = np.array(a_coordinates)

        if a_coordinates.shape[-1] < 2:
            raise ValueError(
                f"`a_coordinates` array should at least have length 2 but it is in shape of" f" {a_coordinates.shape}."
            )

    @classmethod
    def from_xy(cls, a_coordinates: Union[Tuple, List, np.ndarray], **kwargs) -> "KeyPoint2D":
        cls.validate_array(a_coordinates=a_coordinates)

        if len(a_coordinates) == 2:
            keypoint: KeyPoint2D = KeyPoint2D(a_x=a_coordinates[0], a_y=a_coordinates[1], **kwargs)
        elif len(a_coordinates) == 3:
            keypoint: KeyPoint2D = KeyPoint2D(
                a_x=a_coordinates[0], a_y=a_coordinates[1], a_score=a_coordinates[2], **kwargs
            )
        else:
            raise ValueError("Invalid number of coordinates for keypoint.")

        return keypoint


class KeyPoint2DList(BaseList[KeyPoint2D]):
    def __init__(self, a_name: str = "KeyPoint2DList", a_max_size: int = -1, a_items: List[Point2D] = None):
        super().__init__(a_name=a_name, a_max_size=a_max_size, a_items=a_items)

    @classmethod
    def validate_array(cls, a_coordinates: Union[Tuple, List, np.ndarray]) -> np.ndarray:
        if a_coordinates is None or not isinstance(a_coordinates, (Tuple, List, np.ndarray)):
            raise TypeError("The `a_coordinates` should be a `Tuple, List, or np.ndarray`.")

        if not isinstance(a_coordinates, np.ndarray):
            a_coordinates = np.array(a_coordinates)

        if a_coordinates.shape[-1] < 2:
            raise ValueError(
                f"`a_coordinates` array should at least have length 2 but it is in shape of" f" {a_coordinates.shape}."
            )

        if a_coordinates.ndim == 1:
            a_coordinates = a_coordinates[np.newaxis]

        return a_coordinates

    @classmethod
    def from_xy(cls, a_coordinates: Union[Tuple, List, np.ndarray], **kwargs) -> "KeyPoint2DList":
        # Validate array
        coordinates = cls.validate_array(a_coordinates=a_coordinates)

        # Instantiate bounding boxes
        keypoints = KeyPoint2DList()
        keypoints.append(a_item=[KeyPoint2D.from_xy(a_coordinates=coord, **kwargs) for coord in coordinates])
        return keypoints

    def to_xy(self) -> np.ndarray:
        return np.concatenate([keypoint.to_numpy() for keypoint in self.items])
