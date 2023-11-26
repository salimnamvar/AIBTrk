"""2D Image Module

This Python file contains the definition of the Image2D class, which represents a 2D image in the format of
[Height, Width, Channels].

Classes:
    - `Image2D`: Represents a 2D image.

Functions:
    None

Variables:
    None
"""


# region Imported Dependencies
import numpy as np
from brain.util import BaseObject, Size
# endregion Imported Dependencies


class Image2D(BaseObject):
    """Image2D

    This class defines a 2D image in the format of [Height, Width, Channels].

    Attributes
        filename:
            A :type:`str` that specifies the filename of the image.
        data:
            A :class:`np.ndarray` that contains the data of the image as an array.
        width:
            A :type:`int` that specifies the image's width size.
        height:
            A :type:`int` that specifies the image's height size.
        channels:
            A :type:`int` that specifies the number of channels in the image.
    """

    def __init__(self, a_data: np.ndarray, a_filename: str = None, a_name: str = "IMAGE2D") -> None:
        """
        Constructor for the Image2D class.

        Args:
            a_data (np.ndarray):
                A NumPy array containing the image data.
            a_filename (str, optional):
                The filename of the image (default is None).
            a_name (str, optional):
                The name of the Image2D object (default is 'IMAGE2D').

        Returns:
            None:
                The constructor does not return any values.

        Raises:
            TypeError:
                If `a_data` is not a NumPy array, or `a_filename` is not a string.
            ValueError:
                If `a_data` is not 2D or 3D with at least one channel.
        """
        # region Input Checking
        if a_data is not None and not isinstance(a_data, np.ndarray):
            raise TypeError(f"`a_data` argument must be an `np.ndarray` but it's type is `{type(a_data)}`")
        if a_filename is not None and not isinstance(a_filename, str):
            raise TypeError(f"`a_filename` argument must be an `str` but it's type is `{type(a_filename)}`")
        if a_data.ndim not in [2, 3]:
            raise ValueError(
                f"`a_data` array must be 2D or 3D with at least with 1 channel but it is in shape of "
                f"`{a_data.shape}`"
            )
        # endregion Input Checking

        super().__init__(a_name=a_name)
        self.data: np.ndarray = a_data
        self._filename: str = a_filename

    @property
    def width(self) -> int:
        """Image's Width Getter

        This property specifies the width of the image.

        Returns:
            int:
                The width of the image.
        """
        return self.data.shape[1]

    @property
    def height(self) -> int:
        """Image's Height Getter

        This property specifies the height of the image.

        Returns:
            int:
                The height of the image.
        """
        return self.data.shape[0]

    @property
    def size(self) -> Size:
        """Image's Size Getter

        This property specifies the size of the image in [Width, Height] format.

        Returns:
            Size:
                The size of the image as :class:`Size`.
        """
        return Size(self.width, self.height, a_name=f"{self.name} Size")

    @property
    def channels(self) -> int:
        """Image's Channel Getter

        This property specifies the number of channels in the image.

        Returns:
            int:
                The number of channels in the image.
        """
        if self.data.ndim == 2:
            return 1
        else:
            return self.data.shape[2]

    def to_dict(self) -> dict:
        """
        Convert the Image2D object to a dictionary representation.

        This method creates a dictionary where the key is the object's name and the value is the image data.

        Returns:
            dict:
                A dictionary representation of the Image2D object.
        """
        dic = {self.name: self.data}
        return dic
