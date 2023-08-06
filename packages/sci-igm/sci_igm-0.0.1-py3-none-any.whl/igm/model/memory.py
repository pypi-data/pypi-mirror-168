import math
from typing import Optional

from .percentage import Percentage
from .size import SizeScale


class UsedPercentage(Percentage):
    pass


class FreePercentage(Percentage):
    pass


class AvailPercentage(Percentage):
    pass


class MemoryStatus:
    def __init__(self, total, used, free=None, avail=None):
        self.__total = SizeScale(total)
        self.__used = SizeScale(used)
        self.__free = SizeScale(free) if free is not None else \
            SizeScale(self.__total.bytes - self.__used.bytes)
        self.__avail = SizeScale(avail) if avail is not None else None

    @property
    def total(self) -> SizeScale:
        return self.__total

    @property
    def used(self) -> SizeScale:
        return self.__used

    @property
    def free(self) -> SizeScale:
        return self.__free

    @property
    def used_percentage(self) -> Optional[UsedPercentage]:
        try:
            ratio = self.used.bytes / self.total.bytes
            if math.isnan(ratio):
                raise ZeroDivisionError
        except ZeroDivisionError:
            return None
        else:
            return UsedPercentage(ratio)

    @property
    def free_percentage(self) -> Optional[FreePercentage]:
        try:
            ratio = self.free.bytes / self.total.bytes
            if math.isnan(ratio):
                raise ZeroDivisionError
        except ZeroDivisionError:
            return None
        else:
            return FreePercentage(self.free.bytes / self.total.bytes)

    @property
    def avail(self) -> Optional[SizeScale]:
        return self.__avail

    @property
    def avail_percentage(self) -> Optional[AvailPercentage]:
        if self.__avail is not None:
            try:
                ratio = self.avail.bytes / self.total.bytes
                if math.isnan(ratio):
                    raise ZeroDivisionError
            except ZeroDivisionError:
                return None
            else:
                return AvailPercentage(ratio)
        else:
            return None

    def __bool__(self):
        return bool(self.total)

    def __repr__(self):
        if not self:
            return f'<{type(self).__name__} total: {self.total}>'
        else:
            if self.__avail is not None:
                return f'<{type(self).__name__} total: {self.total}, ' \
                       f'used: {self.used} ({self.used_percentage}), ' \
                       f'free: {self.free} ({self.free_percentage}), ' \
                       f'avail: {self.avail} ({self.avail_percentage})>'
            else:
                return f'<{type(self).__name__} total: {self.total}, ' \
                       f'used: {self.used} ({self.used_percentage}), ' \
                       f'free: {self.free} ({self.free_percentage})>'
