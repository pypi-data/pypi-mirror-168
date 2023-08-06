import platform

from .type import OSType
from ...model import MappingBasedModel


def get_os_info():
    return {
        'os': OSType.loads(platform.system()),
        'version': platform.version(),
        'release': platform.release(),
        'node': platform.node(),
    }


class OS(MappingBasedModel):
    def __init__(self, data: dict):
        MappingBasedModel.__init__(self, data)

    @property
    def type(self) -> OSType:
        return OSType.loads(self['os'])

    @property
    def node(self):
        return self['node']

    @property
    def version(self):
        return self['version']

    @property
    def release(self):
        return self['release']

    def _str_format(self):
        return f'<{type(self).__name__} {self.type}, {self.version}, node: {self.node!r}>'

    def __str__(self):
        return self._str_format()

    def __repr__(self):
        return self._str_format()
