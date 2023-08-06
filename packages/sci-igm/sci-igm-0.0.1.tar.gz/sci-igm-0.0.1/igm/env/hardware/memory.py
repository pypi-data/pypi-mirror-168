import time
from functools import lru_cache

import psutil

from ...model import MemoryStatus


@lru_cache()
def _get_memory_info(ttl_hash):
    _ = ttl_hash
    return {
        'virtual': dict(psutil.virtual_memory()._asdict()),
        'swap': dict(psutil.swap_memory()._asdict()),
    }


def get_memory_info():
    from .base import RESOURCE_TIMEOUT
    return _get_memory_info(int(time.time() // RESOURCE_TIMEOUT))


class VirtualMemory(MemoryStatus):
    def __init__(self, data):
        virtual = data['virtual']
        MemoryStatus.__init__(self, virtual['total'], virtual['used'], virtual['free'], virtual['available'])


class SwapMemory(MemoryStatus):
    def __init__(self, data):
        swap = data['swap']
        MemoryStatus.__init__(self, swap['total'], swap['used'], swap['free'])
