import re
from typing import Union

from .comparable import Comparable

PERCENTAGE_REGEXP = re.compile(r'^\s*(?P<percentage>[+\-]?(\d+(\.\d*)?|\d*(\.\d+)?))\s*%\s*$')


class Percentage(Comparable):
    def __init__(self, percentage: Union['Percentage', int, float, str]):
        if isinstance(percentage, Percentage):
            self.__ratio = percentage.__ratio
        elif isinstance(percentage, (int, float)):
            self.__ratio = float(percentage)
        elif isinstance(percentage, str):
            match = PERCENTAGE_REGEXP.fullmatch(percentage)
            if match:
                self.__ratio = float(match.group('percentage')) / 100
            else:
                raise ValueError(f'Invalid percentage string - {percentage!r}.')
        else:
            raise TypeError(f'Unknown percentage type - {percentage!r}.')

    def _value(self):
        return self.__ratio

    @property
    def ratio(self) -> float:
        return self.__ratio

    @property
    def percentage(self) -> float:
        return self.__ratio * 100

    def _str_format(self):
        return f'{self.__ratio * 100:.2f}%'

    def __int__(self) -> int:
        return int(self.__ratio)

    def __float__(self) -> float:
        return self.__ratio

    def __str__(self):
        return self._str_format()

    def __repr__(self):
        return f'<{type(self).__name__} {self._str_format()}>'
