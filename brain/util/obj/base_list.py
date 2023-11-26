"""Base List Module

This module defines the `BaseList` class, a generic class representing a list of objects of type `T`.

Classes:
    BaseList (Generic[T], ABC):
        A generic class representing a list of objects of type `T`.

Variables:
    T (TypeVar):
        A type variable used in generic classes. `T` represents the element type of the generic class,
        typically used in generic classes like :class:`BaseList`.

Functions:
    None
"""


# region Imported Dependencies
import pprint
from abc import ABC
from copy import deepcopy
from typing import TypeVar, Generic, List, Union
# endregion Imported Dependencies


T = TypeVar("T")
"""
A type variable used in generic classes.

`T` represents the element type of the generic class and is typically used in generic classes like 
:class:`BaseList`.
"""


class BaseList(Generic[T], ABC):
    """Base List

    The `BaseList` class represents a list of objects of type `T`.

    Attributes:
        name (str):
            A :type:`string` that specifies the name of the `BaseList` instance.
        _max_size (int):
            An integer representing the maximum size of the list (default is -1, indicating no size limit).
        _items (List[T]):
            A list of objects of type `T` contained within the `BaseList`.
    """

    def __init__(self, a_name: str = "ObjectList", a_max_size: int = -1, a_items: List[T] = None):
        """
        Constructor for the `BaseList` class.

        Args:
            a_name (str, optional):
                A :type:`string` that specifies the name of the `BaseList` instance (default is 'Objects').
            a_max_size (int, optional):
                An :type:`int` representing the maximum size of the list (default is -1, indicating no size limit).
            a_items (List[T], optional):
                A list of objects of type :class:`T` to initialize the `BaseList` (default is None).

        Returns:
            None: The constructor does not return any values.
        """
        self.name: str = a_name
        self._max_size: int = a_max_size
        self._items: List[T] = []

        if a_items is not None:
            self.append(a_item=a_items)

    @property
    def name(self) -> str:
        """Instance Name Getter

        This property specifies the name of the class object.

        Returns
            str: This property returns a :type:`string` as the name of the class object.
        """
        return self._name

    @name.setter
    def name(self, a_name: str = "BASE_LIST") -> None:
        """Instance Name Setter

        This setter is used to set the name of the class object.

        Args:
            a_name (str): A :type:`string` that specifies the class object's name.

        Returns:
            None
        """
        self._name = a_name.upper().replace(" ", "_")

    def to_dict(self) -> List[dict]:
        """
        Convert the `BaseList` to a list of dictionaries.

        This method iterates through the objects in the `BaseList` and converts each object to a dictionary.

        Returns:
            List[dict]: A list of dictionaries, where each dictionary represents an object in the `BaseList`.
        """
        dict_items = []
        for item in self._items:
            dict_items.append(item.to_dict())
        return dict_items

    def to_str(self) -> str:
        """
        Convert the `BaseList` to a formatted string.

        This method converts the `BaseList` into a human-readable string representation by
        using the :class:`pprint.pformat` function on the result of `to_dict`.

        Returns:
            str: A formatted string representing the `BaseList`.
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """
        Return a string representation of the `BaseList` object.

        This method returns a string representation of the `BaseList` by calling the `to_str` method.

        Returns:
            str: A string representing the `BaseList` object.
        """
        return self.to_str()

    @property
    def items(self) -> List[T]:
        """
        Get the list of items in the `BaseList`.

        This property provides access to the list of items contained within the `BaseList`.

        Returns:
            List[T]: A :class:`list` of objects of type :class:`T` within the `BaseList`.
        """
        return self._items

    def __getitem__(self, a_index: int) -> T:
        return self._items[a_index]

    def __setitem__(self, a_index: int, a_item: T):
        """
        Get an item from the `BaseList` by index.

        This method allows retrieving an item from the `BaseList` by its index.

        Args:
            a_index (:type:int): The index of the item to retrieve.

        Returns:
            T: The item at the specified index.
        """
        self._items[a_index] = a_item

    def append(self, a_item: Union[T, List[T], "BaseList"], a_removal_strategy: str = "first"):
        """
        Append an item or a list of items to the `BaseList`.

        This method appends an individual item or a list of items to the `BaseList`.

        Args:
            a_item (Union[T, List[T]]): An item or a list of items to append.
            a_removal_strategy (str): The strategy for removing items when the maximum size is reached. Options:
            `first` (default) or `last`.

        Returns:
            None
        """
        if isinstance(a_item, (list, self.__class__)):
            for item in a_item:
                self._append_item(item, a_removal_strategy)
        else:
            self._append_item(a_item, a_removal_strategy)

    def _append_item(self, a_item: T, a_removal_strategy: str = "first") -> None:
        """
        Append an item to the `BaseList` (Internal).

        This internal method appends an item to the `BaseList`, handling size constraints if `_max_size` is set.

        Args:
            a_item (T): The item to append.
            a_removal_strategy (str): The strategy for removing items when the maximum size is reached. Options:
            `first` or `last`.

        Returns:
            None
        """
        if self._max_size != -1 and len(self) >= self._max_size:
            if a_removal_strategy.lower() == "first":
                self._items.pop(0)
            elif a_removal_strategy.lower() == "last":
                self._items.pop()
            else:
                raise ValueError("Invalid removal strategy. Use 'first' or 'last'.")
        self._items.append(a_item)

    def __delitem__(self, a_index: int):
        """
        Delete an item from the `BaseList` by index.

        This method allows deleting an item from the `BaseList` by its index.

        Args:
            a_index (int): The index of the item to delete.

        Returns:
            None
        """
        del self._items[a_index]

    def copy(self) -> "BaseList[T]":
        """
        Create a deep copy of the `BaseList`.

        This method creates a deep copy of the `BaseList`, including a copy of all contained items.

        Returns:
            BaseList[T]: A duplicated instance of the class.
        """
        return deepcopy(self)

    def __len__(self) -> int:
        """
        Get the number of items in the `BaseList`.

        This method returns the number of items contained within the `BaseList`.

        Returns:
            int: The number of items.
        """
        return len(self._items)

    def clear(self) -> None:
        """Clear all items in the list.

        This method resets the list of items to an empty list.

        Returns:
            None

        """
        self._items = []

    def __contains__(self, a_item: T):
        """Check if the list contains the specified item.

        Args:
            a_item (T): The item to check for membership in the list.

        Returns:
            bool: True if the item is found in the list, False otherwise.
        """
        return a_item in self._items

    def pop(self, a_index: int) -> None:
        """
        Removes an item at the specified index in the BaseList.

        This method removes the item at the given index in the BaseList.

        Args:
            a_index (int): The index of the item to be removed.

        Returns:
            None
        """
        self._items.pop(a_index)
