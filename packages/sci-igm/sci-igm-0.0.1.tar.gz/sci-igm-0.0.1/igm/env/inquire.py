from contextlib import contextmanager
from typing import Mapping, Iterator


class UserInquire(Mapping):
    def __init__(self):
        self.__data = {}

    def __getitem__(self, item: str):
        return self.__data[item]

    def __getattr__(self, item: str):
        try:
            return self.__data[item]
        except KeyError:
            raise AttributeError(f'Attribute {item!r} not found.')

    def __len__(self) -> int:
        return len(self.__data)

    def __iter__(self) -> Iterator[str]:
        yield from self.__data

    def __bool__(self):
        return bool(self.__data)

    def __clone(self):
        return {key: value for key, value in self.__data.items()}

    def __put(self, v: Mapping):
        self.__data.clear()
        for key, value in v.items():
            self.__data[key] = value

    @contextmanager
    def _op_with(self, v: Mapping):
        origin_v = self.__clone()
        try:
            self.__put(v)
            yield
        finally:
            self.__put(origin_v)

    def __repr__(self):
        return f'{type(self).__name__}({self.__data!r})'


user = UserInquire()

_USER_OP_WITH = getattr(user, '_op_with')


@contextmanager
def user_inq_with(v: Mapping):
    with _USER_OP_WITH(v):
        yield
