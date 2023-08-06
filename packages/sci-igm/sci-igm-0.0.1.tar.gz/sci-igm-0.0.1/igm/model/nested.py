from collections.abc import Mapping, Sequence
from typing import Iterator, Union


class MappingBasedModel(Mapping):
    def __init__(self, d: dict):
        self.__d = d

    def __getitem__(self, item: str):
        return to_nested_model(self.__d[item])

    def __getattr__(self, item):
        return to_nested_model(self.__d[item])

    def __len__(self) -> int:
        return len(self.__d)

    def __iter__(self) -> Iterator[str]:
        yield from self.__d

    def __str__(self):
        return str(self.__d)

    def __repr__(self):
        return f'{type(self).__name__}({self.__d!r})'

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.__d == other
        elif isinstance(other, MappingBasedModel):
            return self.__d == other.__d
        else:
            return False


class SequenceBasedModel(Sequence):
    def __init__(self, s: Union[list, tuple]):
        self.__s = s

    def __getitem__(self, index):
        return to_nested_model(self.__s[index])

    def __getattr__(self, item: str):
        """
        Get attribute from original object.

        To Support wrapping of named tuple.
        """
        return to_nested_model(getattr(self.__s, item))

    def __len__(self) -> int:
        return len(self.__s)

    def __str__(self):
        return str(self.__s)

    def __repr__(self):
        return f'{type(self).__name__}({self.__s!r})'

    def __eq__(self, other):
        if isinstance(other, (list, tuple)):
            return list(self.__s) == list(other)
        elif isinstance(other, SequenceBasedModel):
            return list(self.__s) == list(other.__s)
        else:
            return False


def to_nested_model(v):
    if isinstance(v, dict):
        return MappingBasedModel(v)
    elif isinstance(v, (list, tuple)):
        return SequenceBasedModel(v)
    else:
        return v
