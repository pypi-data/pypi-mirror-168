import warnings

from hbutils.scale import size_to_bytes, size_to_bytes_str

from .comparable import Comparable


class SizeScale(Comparable):
    def __init__(self, size):
        if isinstance(size, SizeScale):
            self.__bytes = size.__bytes
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.__bytes = size_to_bytes(size)

    def _value(self):
        return self.__bytes

    @property
    def bytes(self) -> int:
        return self.__bytes

    def __bool__(self):
        return bool(self.__bytes)

    def __int__(self) -> int:
        return self.__bytes

    def __index__(self) -> int:
        return self.__bytes

    def _str_format(self):
        return size_to_bytes_str(self.__bytes, precision=2)

    def __str__(self) -> str:
        return self._str_format()

    def __repr__(self):
        return f'<{type(self).__name__} {self._str_format()}>'
