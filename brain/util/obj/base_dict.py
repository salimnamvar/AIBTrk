"""Base Dict Module

This module defines the `BaseDict` class, a generic class representing a dictionary of objects with specified key and
value types.

Classes:
    BaseDict (Generic[T_key, T_value]):
        A generic class representing a dictionary of objects with specified key and value types.

Variables:
    T_key (TypeVar):
        Type variable for keys in a generic context.
        This type variable is used to represent the type of keys in generic classes or functions.

    T_value (TypeVar):
        Type variable for values in a generic context.
        This type variable is used to represent the type of values in generic classes or functions.

Functions:
    None
"""

# region Imported Dependencies
import pprint
from copy import deepcopy
from typing import TypeVar, Generic, Union, List, Dict, KeysView, ValuesView
# endregion Imported Dependencies


T_key = TypeVar("T_key")
"""
Type variable for keys in a generic context.

This type variable is used to represent the type of keys in generic classes or functions.
"""

T_value = TypeVar("T_value")
"""
Type variable for values in a generic context.

This type variable is used to represent the type of values in generic classes or functions.
"""


class BaseDict(Generic[T_key, T_value]):
    """Base Dict

    The `BaseDict` class represents a dictionary of objects with specified key and value types.

    Attributes:
        name (str):
            A :type:`string` that specifies the name of the `BaseDict` instance.
        _max_size (int):
            An integer representing the maximum size of the dictionary (default is -1, indicating no size limit).
        _items (Dict[T_key, T_value]):
            A dictionary of objects with specified key and value types contained within the `BaseDict`.
    """

    def __init__(
            self,
            a_name: str = "BASE_DICT",
            a_max_size: int = -1,
            a_key: Union[T_key, List[T_key]] = None,
            a_value: Union[T_value, List[T_value]] = None,
    ):
        """
        Constructor for the BaseDict class.

        Args:
            a_name (str, optional):
                A string specifying the name of the BaseDict instance (default is 'BASE_DICT').
            a_max_size (int, optional):
                An integer representing the maximum size of the dictionary (default is -1, indicating no size limit).
            a_key (Union[T_key, List[T_key]], optional):
                The key or list of keys to initialize the BaseDict (default is None).
            a_value (Union[T_value, List[T_value]], optional):
                The value or list of values to initialize the BaseDict (default is None).

        Returns:
            None: The constructor does not return any values.

        Raises:
            RuntimeError: If the length of keys and values in the lists is different during initialization.
        """
        self.name: str = a_name
        self._max_size: int = a_max_size
        self._items: Dict[T_key, T_value] = {}

        if a_key is not None and a_value is not None:
            self.append(a_key, a_value)

    @property
    def name(self) -> str:
        """Instance Name Getter

        This property specifies the name of the class object.

        Returns
            str: This property returns a :type:`string` as the name of the class object.
        """
        return self._name

    @name.setter
    def name(self, a_name: str = "BASE_DICT") -> None:
        """Instance Name Setter

        This setter is used to set the name of the class object.

        Args:
            a_name (str): A :type:`string` that specifies the class object's name.

        Returns:
            None
        """
        self._name = a_name.upper().replace(" ", "_")

    def to_dict(self) -> Dict[T_key, T_value]:
        """
        Return a shallow copy of the dictionary.

        Returns:
            Dict[T_key, T_value]: A shallow copy of the dictionary.
        """
        return self._items.copy()

    def to_str(self) -> str:
        """
        Convert the `BaseDict` to a formatted string.

        This method converts the `BaseDict` into a human-readable string representation by
        using the :class:`pprint.pformat` function on the result of `to_dict`.

        Returns:
            str: A formatted string representing the `BaseDict`.
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """
        Return a string representation of the `BaseDict` object.

        This method returns a string representation of the `BaseDict` by calling the `to_str` method.

        Returns:
            str: A string representing the `BaseDict` object.
        """
        return self.to_str()

    @property
    def items(self) -> Dict[T_key, T_value]:
        """
        Get the dictionary of items in the `BaseDict`.

        This property provides access to the dictionary of items contained within the `BaseDict`.

        Returns:
            Dict[T_key, T_value]: A :class:`dict` of objects with specified key and value types within the `BaseDict`.
        """
        return self._items

    def __getitem__(self, a_key: T_key) -> T_value:
        """
        Retrieve the value associated with the given key.

        Args:
            a_key (T_key): The key for which to retrieve the associated value.

        Returns:
            T_value: The value associated with the provided key.
        """
        return self._items[a_key]

    def __setitem__(self, a_key: T_key, a_value: T_value):
        """
        Set the value associated with the given key.

        Args:
            a_key (T_key): The key for which to set the associated value.
            a_value (T_value): The value to be associated with the provided key.

        Returns:
            None
        """
        if a_key in self._items or self._max_size == -1:
            self._items[a_key] = a_value
        elif a_key not in self._items and self._max_size > 0:
            self.append(a_key=a_key, a_value=a_value)
        else:
            raise IndexError(f"The dictionary does not contain the `{a_key}` key.")

    def append(
            self,
            a_key: Union[T_key, List[T_key]],
            a_value: Union[T_value, List[T_value]],
            a_removal_strategy: str = "first",
    ):
        """
        Append key-value pairs to the BaseDict.

        This method appends individual key-value pairs or lists of key-value pairs to the BaseDict.
        If the maximum size is specified, it removes key-value pairs according to the removal strategy.

        Args:
            a_key (Union[T_key, List[T_key]]): The key or list of keys to append.
            a_value (Union[T_value, List[T_value]]): The value or list of values to append.
            a_removal_strategy (str, optional):
                The strategy for removing key-value pairs when the maximum size is reached.
                    Options: 'first' (default) or 'last'.

        Returns:
            None

        Raises:
            ValueError: If an invalid removal strategy is provided.
            RuntimeError: If the length of keys and values in the lists is different.
        """
        if isinstance(a_key, list) and isinstance(a_value, list):
            if len(a_key) != len(a_value):
                raise RuntimeError(
                    f"The length of keys and values must be the same, but they are {len(a_key)}, "
                    f"{len(a_value)} respectively."
                )
            for key, value in zip(a_key, a_value):
                self._append_item(key, value, a_removal_strategy)
        else:
            self._append_item(a_key, a_value, a_removal_strategy)

    def _append_item(self, a_key: T_key, a_value: T_value, a_removal_strategy: str = "first") -> None:
        """
        Append a key-value pair to the BaseDict, handling size constraints.

        This internal method appends a key-value pair to the BaseDict, and if a maximum size is specified,
        it removes a key-value pair according to the removal strategy when the size exceeds the maximum.

        Args:
            a_key (T_key): The key to append.
            a_value (T_value): The value to append.
            a_removal_strategy (str, optional):
                The strategy for removing key-value pairs when the maximum size is reached.
                Options: 'first' (default) or 'last'.

        Returns:
            None

        Raises:
            ValueError: If an invalid removal strategy is provided.
        """
        if self._max_size != -1 and len(self) >= self._max_size:
            if a_removal_strategy.lower() == "first":
                first_key = next(iter(self._items))
                self._items.pop(first_key)
            elif a_removal_strategy.lower() == "last":
                self._items.popitem()
            else:
                raise ValueError("Invalid removal strategy. Use 'first' or 'last'.")
        self._items[a_key] = a_value

    def __delitem__(self, a_key: T_key):
        """
        Remove the key-value pair associated with the given key.

        Args:
            a_key (T_key): The key for which to remove the associated key-value pair.

        Returns:
            None
        """
        del self._items[a_key]

    def copy(self) -> "BaseDict[T_key, T_value]":
        """
        Create a deep copy of the BaseDict.

        This method creates a deep copy of the BaseDict, including a copy of all contained key-value pairs.

        Returns:
            BaseDict[T_key, T_value]: A duplicated instance of the class.
        """
        return deepcopy(self)

    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the BaseDict.

        Returns:
            int: The number of key-value pairs in the BaseDict.
        """
        return len(self._items)

    def clear(self) -> None:
        """
        Clear all key-value pairs in the BaseDict.

        This method resets the dictionary of key-value pairs to an empty dictionary.

        Returns:
            None
        """
        self._items = {}

    def __contains__(self, a_key: T_key):
        """Check if the BaseDict contains the specified key.

        Args:
            a_key (T_key): The key to check for membership in the BaseDict.

        Returns:
            bool: True if the item is found in the BaseDict, False otherwise.
        """
        return a_key in self._items

    def keys(self) -> KeysView[T_key]:
        """
        Return a view of the keys in the BaseDict.

        This method returns a view object displaying a list of all the keys in the BaseDict.

        Returns:
            KeysView[T_key]: A view object displaying the keys.
        """
        return self._items.keys()

    def values(self) -> ValuesView[T_value]:
        """
        Return a view of the values in the BaseDict.

        This method returns a view object displaying a list of all the values in the BaseDict.

        Returns:
            ValuesView[T_value]: A view object displaying the values.
        """
        return self._items.values()

    def pop(self, a_key: T_key) -> None:
        """
        Remove the item with the specified key.

        This method removes the item with the specified key.

        Args:
            a_key (T_key): The key of the item to remove.

        Returns:
            None
        """
        self._items.pop(a_key)