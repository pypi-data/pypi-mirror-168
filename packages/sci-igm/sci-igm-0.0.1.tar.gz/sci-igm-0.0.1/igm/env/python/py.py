import platform
from enum import Enum, unique

from . import Pip
from ...model import VersionInfo, MappingBasedModel


class PythonVersion(VersionInfo):
    pass


@unique
class PythonImplement(Enum):
    CPYTHON = 'CPython'
    IRONPYTHON = 'IronPython'
    JYTHON = 'Jython'
    PYPY = 'PyPy'

    @classmethod
    def loads(cls, x) -> 'PythonImplement':
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
        return self.value

    def __repr__(self):
        return f'<{type(self).__name__} {self.value}>'


def get_python_info():
    return {
        'version': PythonVersion(platform.python_version()),
        'implement': PythonImplement.loads(platform.python_implementation()),
    }


class Python(MappingBasedModel):
    def __init__(self, data: dict):
        MappingBasedModel.__init__(self, data)

    @property
    def version(self) -> PythonVersion:
        return self['version']

    @property
    def implement(self) -> PythonImplement:
        return self['implement']

    @property
    def pip(self) -> Pip:
        return Pip()

    def __str__(self):
        return f'{self.implement} {self.version}'

    def __repr__(self):
        return f'<{type(self).__name__}, version: {self.version}, implement: {self.implement}>'
