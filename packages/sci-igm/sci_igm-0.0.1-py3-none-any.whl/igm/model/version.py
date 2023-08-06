from typing import Callable, Union

from pkg_resources import parse_version

from .comparable import Comparable

_Version = type(parse_version('0.0.1'))


class VersionInfo(Comparable):
    """
    Overview:
        Class for wrapping version information.

    .. warning::
        This class is not immutable for its designing for dynamic comparison and boolean check.
        Please pay attention when use it.
    """

    def __init__(self, v: Union['VersionInfo', _Version, Callable, str, tuple, int]):
        """
        Constructor of :class:`VersionInfo`.

        :param v: Version information, can be a :class:`VersionInfo`, version, function, str, \
            tuple or integer.
        """
        if isinstance(v, VersionInfo):
            self._version, self._func = v._version, v._func
        elif isinstance(v, _Version) or v is None:
            self._version, self._func = v, None
        elif callable(v):
            self._version, self._func = None, v
        elif isinstance(v, str):
            VersionInfo.__init__(self, parse_version(v))
        elif isinstance(v, tuple):
            VersionInfo.__init__(self, '.'.join(map(str, v)))
        elif isinstance(v, int):
            VersionInfo.__init__(self, str(v))
        else:
            raise TypeError(f'Unknown version type - {repr(v)}.')

    @property
    def _actual_version(self):
        if self._func is None:
            return self._version
        else:
            return VersionInfo(self._func())._version

    def _value(self):
        return self._actual_version

    def _cmp_precondition(self, other):
        return Comparable._cmp_precondition(self, other) and (self and other)

    def __eq__(self, other):
        return self._actual_version == VersionInfo(other)._actual_version

    def __bool__(self):
        return bool(self._actual_version)

    def __str__(self):
        return str(self._actual_version) if self._actual_version else ''

    def __repr__(self):
        return f'<{type(self).__name__} {self._actual_version}>'
