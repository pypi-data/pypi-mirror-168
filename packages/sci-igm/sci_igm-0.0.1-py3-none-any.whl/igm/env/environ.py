import os
from collections.abc import Mapping
from typing import Optional, Iterator


class Env(Mapping):
    @classmethod
    def _getitem(cls, item) -> Optional[str]:
        return os.environ.get(item, None)

    def __getitem__(self, item) -> Optional[str]:
        return self._getitem(item)

    def __getattr__(self, item) -> Optional[str]:
        return self._getitem(item)

    def __len__(self) -> int:
        return len(os.environ)

    def __iter__(self) -> Iterator[str]:
        yield from os.environ

    def __repr__(self) -> str:
        return str(os.environ)


env = Env()
