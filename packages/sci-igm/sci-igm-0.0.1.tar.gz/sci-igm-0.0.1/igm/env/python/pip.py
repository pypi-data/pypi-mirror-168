from hbutils.system import package_version

from igm.model import VersionInfo


class PipVersion(VersionInfo):
    pass


class PipPackage:
    def __init__(self, name, version):
        self.__name = name
        self.__version = PipVersion(version)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self) -> PipVersion:
        return self.__version

    def __str__(self):
        return f'{self.name}=={self.version}'

    def __repr__(self):
        return f'<{type(self).__name__} {self.name}, version: {self.version}>'


class Pip:
    def __call__(self, name: str) -> PipPackage:
        return PipPackage(name, package_version(name))

    @property
    def version(self):
        return self('pip').version

    def __repr__(self):
        return f'<{type(self).__name__} version: {self.version}>'
