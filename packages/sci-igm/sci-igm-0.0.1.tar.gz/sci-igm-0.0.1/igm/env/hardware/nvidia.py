import os
import subprocess
import time
import warnings
from functools import lru_cache

import xmltodict
from hbutils.system import which


class NvidiaSmiNotFound(Exception):
    pass


class NvidiaSmiFailed(Exception):
    pass


@lru_cache()
def _nvidia_smi_info(nvidia_smi, ttl_hash):
    _ = ttl_hash
    process = subprocess.Popen([nvidia_smi, '-x', '-q'], stdout=subprocess.PIPE)
    (stdout, stderr) = process.communicate()
    exit_code = process.wait()

    if exit_code:
        raise NvidiaSmiFailed(exit_code, stderr)
    if stderr and stderr.strip():
        warnings.warn(f'Stderr from nvidia-smi:{os.linesep}'
                      f'{stderr}')

    return xmltodict.parse(stdout)


def get_nvidia_info():
    from .base import RESOURCE_TIMEOUT
    nvidia_smi = which('nvidia-smi')
    if not nvidia_smi:
        raise NvidiaSmiNotFound('nvidia-smi not found in current environment.')

    return _nvidia_smi_info(nvidia_smi, int(time.time() // RESOURCE_TIMEOUT))
