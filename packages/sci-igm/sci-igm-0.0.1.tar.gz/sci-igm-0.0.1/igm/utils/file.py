import mimetypes
import os
from itertools import chain


def _iter_extensions():
    for n1, n2 in chain(*map(
            lambda x: x.items(),
            [mimetypes.types_map, mimetypes.common_types, mimetypes.encodings_map, mimetypes.suffix_map]
    )):
        if n1.startswith('.'):
            yield n1
        if n2.startswith('.'):
            yield n2


def get_file_ext(filename) -> str:
    filename = os.path.normcase(filename)

    ext = ''
    for exist_ext in _iter_extensions():
        if filename.endswith(exist_ext) and len(exist_ext) > len(ext):
            ext = exist_ext

    if not ext:
        _, ext = os.path.splitext(filename)

    return ext


def splitext(filename):
    ext = get_file_ext(filename)
    if ext:
        return filename[:-len(ext)], ext
    else:
        return filename, ''
