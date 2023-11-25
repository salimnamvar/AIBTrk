"""Base Object Utility

    This module provides the :class:`BaseObject`, :class:`BaseObjectList`, :class:`BaseObjectDict` classes,
    which serve as the fundamental building blocks for handling objects, lists, and dictionaries.
"""

# region Imported Dependencies
import pprint
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Generic, TypeVar, Union, Dict, KeysView, ValuesView

# endregion Imported Dependencies


# region Base Object----------------------------------------------------------------------------------------------------
class BaseObject(ABC):
    """Base Object

    The Base Object is a principle basic object class that has the common features and functionalities in handling
    an object.

    Attributes
        name:
            A :type:`string` that specifies the class object name.
    """

    def __init__(self, a_name: str = "Object") -> None:
        """Base Object

        This is a constructor that create an instance of the BaseObject object.

        Args
            a_name:
                A :type:`string` that specifies the name of the object.

        Returns
                The constructor does not return any values.
        """
        self.name: str = a_name

    @property
    def name(self) -> str:
        """Instance Name Getter

        This property specifies the name of the class object.

        Returns
            str: This property returns a :type:`string` as the name of the class object.
        """
        return self._name

    @name.setter
    def name(self, a_name: str = "BASE_OBJECT") -> None:
        """Instance Name Setter

        This setter is used to set the name of the class object.

        Args:
            a_name (str): A :type:`string` that specifies the class object's name.

        Returns:
            None
        """
        self._name = a_name.upper().replace(" ", "_")

    @abstractmethod
    def to_dict(self) -> dict:
        """To Dictionary

        This method represent the object as a dictionary. The method should be overridden.

        Returns
            dic:
                A dictionary that contains the object elements.
        """
        NotImplementedError("Subclasses must implement `to_dict`")

    def to_str(self) -> str:
        """To String

        This method represent the object as a string.

        Returns
            message:
                A :type:`string` as the object representative.
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """Represent Instance

        This method represents the object of the class as a string.

        Returns
            message:
                This method returns a :type:`string` as the representation of the class object.
        """
        return self.to_str()

    def copy(self) -> "BaseObject":
        """Copy Instance

        This method copies the object deeply.

        Returns
            The method returns the duplicated object of the class.
        """
        return deepcopy(self)


# endregion Base Object


# region Base List------------------------------------------------------------------------------------------------------
T = TypeVar("T")
"""
A type variable used in generic classes.

`T` represents the element type of the generic class and is typically used in generic classes like 
:class:`BaseObjectList`.
"""


class BaseObjectList(Generic[T], ABC):
    """Base Object List

    The `BaseObjectList` class represents a list of objects of type `T`.

    Attributes:
        name (str):
            A :type:`string` that specifies the name of the `BaseObjectList` instance.
        _max_size (int):
            An integer representing the maximum size of the list (default is -1, indicating no size limit).
        _items (List[T]):
            A list of objects of type `T` contained within the `BaseObjectList`.
    """

    def __init__(self, a_name: str = "ObjectList", a_max_size: int = -1, a_items: List[T] = None):
        """
        Constructor for the `BaseObjectList` class.

        Args:
            a_name (str, optional):
                A :type:`string` that specifies the name of the `BaseObjectList` instance (default is 'Objects').
            a_max_size (int, optional):
                An :type:`int` representing the maximum size of the list (default is -1, indicating no size limit).
            a_items (List[T], optional):
                A list of objects of type :class:`T` to initialize the `BaseObjectList` (default is None).

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
    def name(self, a_name: str = "BASE_OBJECT_LIST") -> None:
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
        Convert the `BaseObjectList` to a list of dictionaries.

        This method iterates through the objects in the `BaseObjectList` and converts each object to a dictionary.

        Returns:
            List[dict]: A list of dictionaries, where each dictionary represents an object in the `BaseObjectList`.
        """
        dict_items = []
        for item in self._items:
            dict_items.append(item.to_dict())
        return dict_items

    def to_str(self) -> str:
        """
        Convert the `BaseObjectList` to a formatted string.

        This method converts the `BaseObjectList` into a human-readable string representation by
        using the :class:`pprint.pformat` function on the result of `to_dict`.

        Returns:
            str: A formatted string representing the `BaseObjectList`.
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """
        Return a string representation of the `BaseObjectList` object.

        This method returns a string representation of the `BaseObjectList` by calling the `to_str` method.

        Returns:
            str: A string representing the `BaseObjectList` object.
        """
        return self.to_str()

    @property
    def items(self) -> List[T]:
        """
        Get the list of items in the `BaseObjectList`.

        This property provides access to the list of items contained within the `BaseObjectList`.

        Returns:
            List[T]: A :class:`list` of objects of type :class:`T` within the `BaseObjectList`.
        """
        return self._items

    def __getitem__(self, a_index: int) -> T:
        return self._items[a_index]

    def __setitem__(self, a_index: int, a_item: T):
        """
        Get an item from the `BaseObjectList` by index.

        This method allows retrieving an item from the `BaseObjectList` by its index.

        Args:
            a_index (:type:int): The index of the item to retrieve.

        Returns:
            T: The item at the specified index.
        """
        self._items[a_index] = a_item

    def append(self, a_item: Union[T, List[T], "BaseObjectList"], a_removal_strategy: str = "first"):
        """
        Append an item or a list of items to the `BaseObjectList`.

        This method appends an individual item or a list of items to the `BaseObjectList`.

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
        Append an item to the `BaseObjectList` (Internal).

        This internal method appends an item to the `BaseObjectList`, handling size constraints if `_max_size` is set.

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
        Delete an item from the `BaseObjectList` by index.

        This method allows deleting an item from the `BaseObjectList` by its index.

        Args:
            a_index (int): The index of the item to delete.

        Returns:
            None
        """
        del self._items[a_index]

    def copy(self) -> "BaseObjectList[T]":
        """
        Create a deep copy of the `BaseObjectList`.

        This method creates a deep copy of the `BaseObjectList`, including a copy of all contained items.

        Returns:
            BaseObjectList[T]: A duplicated instance of the class.
        """
        return deepcopy(self)

    def __len__(self) -> int:
        """
        Get the number of items in the `BaseObjectList`.

        This method returns the number of items contained within the `BaseObjectList`.

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
        Removes at the specified index in the BaseObjectList.

        This method removes the item at the given index in the BaseObjectList.

        Args:
            a_index (int): The index of the item to be removed.

        Returns:
            None
        """
        self._items.pop(a_index)


# endregion Base List


# region Base Dictionary------------------------------------------------------------------------------------------------
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


class BaseObjectDict(Generic[T_key, T_value]):
    """Base Object Dictionary

    The `BaseObjectDict` class represents a dictionary of objects with specified key and value types.

    Attributes:
        name (str):
            A :type:`string` that specifies the name of the `BaseObjectDict` instance.
        _max_size (int):
            An integer representing the maximum size of the dictionary (default is -1, indicating no size limit).
        _items (Dict[T_key, T_value]):
            A dictionary of objects with specified key and value types contained within the `BaseObjectDict`.
    """

    def __init__(
        self,
        a_name: str = "BASE_OBJECT_DICT",
        a_max_size: int = -1,
        a_key: Union[T_key, List[T_key]] = None,
        a_value: Union[T_value, List[T_value]] = None,
    ):
        """
        Constructor for the BaseObjectDict class.

        Args:
            a_name (str, optional):
                A string specifying the name of the BaseObjectDict instance (default is 'BASE_OBJECT_DICT').
            a_max_size (int, optional):
                An integer representing the maximum size of the dictionary (default is -1, indicating no size limit).
            a_key (Union[T_key, List[T_key]], optional):
                The key or list of keys to initialize the BaseObjectDict (default is None).
            a_value (Union[T_value, List[T_value]], optional):
                The value or list of values to initialize the BaseObjectDict (default is None).

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
    def name(self, a_name: str = "BASE_OBJECT_DICT") -> None:
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
        Convert the `BaseObjectDict` to a formatted string.

        This method converts the `BaseObjectDict` into a human-readable string representation by
        using the :class:`pprint.pformat` function on the result of `to_dict`.

        Returns:
            str: A formatted string representing the `BaseObjectDict`.
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """
        Return a string representation of the `BaseObjectDict` object.

        This method returns a string representation of the `BaseObjectDict` by calling the `to_str` method.

        Returns:
            str: A string representing the `BaseObjectDict` object.
        """
        return self.to_str()

    @property
    def items(self) -> Dict[T_key, T_value]:
        """
        Get the dictionary of items in the `BaseObjectDict`.

        This property provides access to the dictionary of items contained within the `BaseObjectDict`.

        Returns:
            Dict[T_key, T_value]: A :class:`dict` of objects with specified key and value types within the `BaseObjectDict`.
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
        Append key-value pairs to the BaseObjectDict.

        This method appends individual key-value pairs or lists of key-value pairs to the BaseObjectDict.
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
        Append a key-value pair to the BaseObjectDict, handling size constraints.

        This internal method appends a key-value pair to the BaseObjectDict, and if a maximum size is specified,
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

    def copy(self) -> "BaseObjectDict[T_key, T_value]":
        """
        Create a deep copy of the BaseObjectDict.

        This method creates a deep copy of the BaseObjectDict, including a copy of all contained key-value pairs.

        Returns:
            BaseObjectDict[T_key, T_value]: A duplicated instance of the class.
        """
        return deepcopy(self)

    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the BaseObjectDict.

        Returns:
            int: The number of key-value pairs in the BaseObjectDict.
        """
        return len(self._items)

    def clear(self) -> None:
        """
        Clear all key-value pairs in the BaseObjectDict.

        This method resets the dictionary of key-value pairs to an empty dictionary.

        Returns:
            None
        """
        self._items = {}

    def __contains__(self, a_key: T_key):
        """Check if the BaseObjectDict contains the specified key.

        Args:
            a_key (T_key): The key to check for membership in the BaseObjectDict.

        Returns:
            bool: True if the item is found in the BaseObjectDict, False otherwise.
        """
        return a_key in self._items

    def keys(self) -> KeysView[T_key]:
        """
        Return a view of the keys in the BaseObjectDict.

        This method returns a view object displaying a list of all the keys in the BaseObjectDict.

        Returns:
            KeysView: A view object displaying the keys.
        """
        return self._items.keys()

    def values(self) -> ValuesView[T_value]:
        """
        Return a view of the values in the BaseObjectDict.

        This method returns a view object displaying a list of all the values in the BaseObjectDict.

        Returns:
            ValuesView: A view object displaying the values.
        """
        return self._items.values()


# endregion Base Dictionary
