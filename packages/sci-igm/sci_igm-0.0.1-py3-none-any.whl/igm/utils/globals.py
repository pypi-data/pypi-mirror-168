import inspect


def get_globals(stacklevel: int = 1) -> dict:
    """
    Overview:
        Get globals dictionary from the outside scope.

    :param stacklevel: Level of stacks when queried, default is ``1`` which means start from the outside scope of \
        current frame.
    :return: Globals dictionary object.
    """
    frame = inspect.currentframe().f_back
    for i in range(stacklevel):
        frame = frame.f_back

    return frame.f_globals


def get_global_env(name, default=None, stacklevel: int = 1, recursive: bool = True):
    """
    Overview:
        Get global variable from the outside scope.

    :param name: Name of the variable.
    :param default: Default value when not found.
    :param stacklevel: Level of stacks when queried, default is ``1`` which means start from the outside scope of \
        current frame.
    :param recursive: Find variable recursively.
    :return: Value of the global variable.
    """
    frame = inspect.currentframe().f_back
    for i in range(stacklevel):
        frame = frame.f_back

    while frame is not None:
        if name in frame.f_globals:
            return frame.f_globals[name]

        if not recursive:
            break
        else:
            frame = frame.f_back

    return default
