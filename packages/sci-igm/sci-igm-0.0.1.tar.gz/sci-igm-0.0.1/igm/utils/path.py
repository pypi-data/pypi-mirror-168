import os.path


def normpath(path: str, *paths: str) -> str:
    """
    Overview:
        Normalize the path to a unique format which is comparable by ``==``.

    :param path: First path segment.
    :param paths: Following segments.
    :return: Full absolute path.
    
    Examples::
        >>> from igm.utils import normpath
        >>> normpath('./file')
        '/home/user/igm/file'
        >>> normpath('/home/file')
        '/home/file'
        >>> normpath('~/file')
        '/home/user/file'
    """
    return os.path.normcase(os.path.normpath(os.path.abspath(
        os.path.expandvars(os.path.expanduser(
            os.path.join(path, *paths)
        ))
    )))


def _samepath(src, dst) -> bool:
    """
    Copied from ``shutils._samepath``.

    :param src: Source path.
    :param dst: Destination path.
    :return: Same or not.
    """
    # Macintosh, Unix.
    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False

    # All other platforms: check for same pathname.
    return (os.path.normcase(os.path.abspath(src)) ==
            os.path.normcase(os.path.abspath(dst)))
