from typing import Optional

from hbutils.string import plural_word

from .hardware import get_cpu_info, CPUSet, CUDA, GPUCollection, get_memory_info, SwapMemory, VirtualMemory, \
    get_nvidia_info
from .hardware.nvidia import NvidiaSmiNotFound
from .internet import Internet, internet
from .os import OS, get_os_info
from .python import get_python_info, Python, Pip


class SystemInfo:
    @property
    def cpu(self) -> CPUSet:
        return CPUSet(get_cpu_info())

    @property
    def memory(self) -> VirtualMemory:
        return VirtualMemory(get_memory_info())

    @property
    def swap(self) -> SwapMemory:
        return SwapMemory(get_memory_info())

    @property
    def cuda(self) -> Optional[CUDA]:
        try:
            return CUDA(get_nvidia_info())
        except NvidiaSmiNotFound:
            return None

    @property
    def gpu(self) -> Optional[GPUCollection]:
        cuda = self.cuda
        if cuda:
            return cuda.gpus
        else:
            return None

    @property
    def internet(self) -> Internet:
        return internet

    @property
    def os(self) -> OS:
        return OS(get_os_info())

    @property
    def python(self) -> Python:
        return Python(get_python_info())

    @property
    def pip(self) -> Pip:
        return self.python.pip

    def __repr__(self):
        _python = f'{self.python.implement} {self.python.version} on {self.os.type}'
        _common = f'{plural_word(self.cpu.num, "core")} {self.memory.total}'
        if self.gpu:
            _common += f' with {plural_word(self.gpu.num, "gpu")}'

        return f'<{type(self).__name__} {_python}, {_common}>'


sys = SystemInfo()
