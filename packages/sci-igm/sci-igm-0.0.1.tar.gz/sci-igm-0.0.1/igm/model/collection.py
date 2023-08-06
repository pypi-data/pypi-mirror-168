from collections.abc import Sequence
from typing import List, TypeVar

ItemType = TypeVar('ItemType')


class GenericCollection(Sequence):
    def __init__(self, items: List[ItemType]):
        self.__items = items

    @property
    def num(self):
        return len(self)

    def __getitem__(self, index):
        return self.__items[index]

    def __len__(self) -> int:
        return len(self.__items)

    def __bool__(self) -> bool:
        return bool(self.__items)

    def __repr__(self):
        return f'{type(self).__name__}({self.__items!r})'
