import statistics
import time
from enum import Enum, unique
from functools import lru_cache
from typing import List, Optional

import cpuinfo
import psutil
from hbutils.string import plural_word
from hbutils.system import is_linux

from ...model import GenericCollection, Percentage, MappingBasedModel


@lru_cache()
def _init_percent():
    _ = psutil.cpu_percent(percpu=True)


@lru_cache()
def _get_cpu_info(ttl_hash):
    _ = ttl_hash
    _init_percent()

    info = cpuinfo.get_cpu_info()
    cnt = info['count']

    # noinspection PyTypeChecker
    percents: List[float] = psutil.cpu_percent(percpu=True)
    assert cnt == len(percents), \
        f'{plural_word(cnt, "cpu")} expected, but {plural_word(len(percents), "percentage")} found.'

    # noinspection PyTypeChecker
    freq: List = psutil.cpu_freq(percpu=True)
    if not is_linux() and len(freq) == 1 and cnt > 1:  # for os except linux
        freq = [freq[0] for _ in range(cnt)]
    assert cnt == len(freq), \
        f'{plural_word(cnt, "cpu")} expected, but {plural_word(len(freq), "frequency")} found.'

    return {
        **info,
        **{
            'cpus': [
                {
                    'percentage': perc,
                    'frequency': freq.current,
                }
                for perc, freq in zip(percents, freq)
            ]
        }
    }


def get_cpu_info():
    from .base import RESOURCE_TIMEOUT
    return _get_cpu_info(int(time.time() // RESOURCE_TIMEOUT))


@unique
class CPUArch(Enum):
    X86_32 = "X86_32"
    X86_64 = "X86_64"
    ARM_8 = "ARM_8"
    ARM_7 = "ARM_7"
    PPC_32 = "PPC_32"
    PPC_64 = "PPC_64"
    SPARC_32 = "SPARC_32"
    SPARC_64 = "SPARC_64"
    S390X = "S390X"
    MIPS_32 = "MIPS_32"
    MIPS_64 = "MIPS_64"
    RISCV_32 = "RISCV_32"
    RISCV_64 = "RISCV_64"

    @classmethod
    def loads(cls, x) -> 'CPUArch':
        if isinstance(x, cls):
            return x
        elif isinstance(x, str):
            return cls[x.upper()]
        else:
            raise TypeError(f'Invalid type of cpu arch - {x!r}.')

    def __eq__(self, other):
        try:
            other = self.loads(other)
        except (KeyError, TypeError):
            return False

        return self.value == other.value

    def __str__(self):
        return self.value.lower()

    def __repr__(self):
        return f'<{type(self).__name__} {self.value.lower()}>'


class CPUInfo(MappingBasedModel):
    def __init__(self, data: dict):
        MappingBasedModel.__init__(self, data)

    @property
    def brand(self) -> str:
        return self['brand_raw']

    @property
    def arch(self) -> Optional['CPUArch']:
        try:
            return CPUArch.loads(self['arch'])
        except (TypeError, KeyError):  # pragma: no cover
            return None


class CPUUsage(Percentage):
    pass


class CPUSet(GenericCollection):
    def __init__(self, data: dict):
        GenericCollection.__init__(self, [CPU(i, item) for i, item in enumerate(data['cpus'])])
        self.info = CPUInfo(data)

    @property
    def brand(self) -> str:
        return self.info.brand

    @property
    def arch(self) -> 'CPUArch':
        return self.info.arch

    @property
    def usage(self) -> CPUUsage:
        return CPUUsage(statistics.mean([c['percentage'] / 100 for c in self]))

    @property
    def frequency(self) -> float:
        return statistics.mean([c['frequency'] for c in self])

    def __repr__(self):
        return f'<{type(self).__name__} {self.brand}, arch: {self.arch}, ' \
               f'{plural_word(len(self), "cpu")}, usage: {self.usage}, freq: {self.frequency:.2f} MHz>'


class CPU(MappingBasedModel):
    def __init__(self, id_: int, data: dict):
        MappingBasedModel.__init__(self, data)
        self.__id = id_

    @property
    def id(self):
        return self.__id

    @property
    def usage(self) -> CPUUsage:
        return CPUUsage(self['percentage'] / 100)

    @property
    def frequency(self) -> float:
        return self['frequency']

    def __repr__(self):
        return f'<{type(self).__name__} #{self.__id}, usage: {self.usage}, freq: {self.frequency:.2f} MHz>'
