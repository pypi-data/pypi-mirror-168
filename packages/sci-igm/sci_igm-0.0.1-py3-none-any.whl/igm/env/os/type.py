from enum import unique, Enum


@unique
class OSType(Enum):
    LINUX = ('Linux', ())
    WINDOWS = ('Windows', ('win',))
    DARWIN = ('macOS', ('darwin', 'mac',))
    JAVA = ('Java', ())

    @classmethod
    def loads(cls, x) -> 'OSType':
        if isinstance(x, cls):
            return x
        elif isinstance(x, str):
            try:
                return cls[x.upper()]
            except KeyError:
                for key, value in cls.__members__.items():
                    name, alias_set = value.value
                    for alias in [name, *alias_set]:
                        if x.upper() == alias.upper():
                            return value
                raise
        else:
            raise TypeError(f'Invalid type of OS - {x!r}.')

    def __eq__(self, other):
        try:
            other = self.loads(other)
        except (KeyError, TypeError):
            return False

        return self.value == other.value

    def __str__(self):
        name, alias_set = self.value
        return name

    def __repr__(self):
        name, alias_set = self.value
        return f'<{type(self).__name__} {name}>'
