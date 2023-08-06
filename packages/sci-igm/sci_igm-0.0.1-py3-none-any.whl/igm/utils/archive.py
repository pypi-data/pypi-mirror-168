import mimetypes
import os
import shutil
from typing import Optional

try:
    import rarfile
except ImportError:  # pragma: no cover
    rarfile = None


class RARExtractionNotSupported(Exception):
    pass


def _rar_extract(filename, extract_dir):
    if rarfile is None:
        raise RARExtractionNotSupported('RAR file extraction not supported, '
                                        'please install \'rarfile\' package with your pip.')

    with rarfile.RarFile(filename) as rf:
        rf.extractall(path=extract_dir)


try:
    import py7zr
except ImportError:  # pragma: no cover
    py7zr = None


class SevenZipExtractionNotSupported(Exception):
    pass


def _7z_extract(filename, extract_dir):
    if py7zr is None:
        raise SevenZipExtractionNotSupported('7z file extraction not supported, '
                                             'please install \'py7zr\' package with your pip.')

    with py7zr.SevenZipFile(filename) as rf:
        rf.extractall(path=extract_dir)


shutil.register_unpack_format('rar', ['.rar'], _rar_extract, [], 'WinRAR file')
shutil.register_unpack_format('7z', ['.7z'], _7z_extract, [], '7z file')


def unpack_archive(filename, dstpath, fmt: Optional[str] = None):
    """
    Overview:
        Extract from all kind of archive files, including ``.zip``, ``.tar``, ``.tar.gz``, ``.tar.xz``, ``.tar.bz2``, \
        ``.rar`` (requires ``rarfile`` package) and ``.7z`` (requires ``py7zr`` package``).

    :param filename: Filename of the archive file.
    :param dstpath: Destination path of the extracted file.
    :param fmt: Format of the file, default is ``None`` which means the format will be auto-detected with ``filename``.
    :return: Destination path of this extraction.

    .. note::
        Password is not supported at present.
    """
    shutil.unpack_archive(filename, dstpath, fmt)
    return dstpath


def get_archive_type(filename: str, content_type: Optional[str] = None) -> Optional[str]:
    """
    Overview:
        Get archive file type of the given ``filename`` and ``content_type``.

    :param filename: Filename.
    :param content_type: Content-Type information from remote.
    :return: Archive format, can be used in :func:`shutils.unpack_archive` method.
    """
    if content_type:
        ext_guess = mimetypes.guess_extension(content_type)
        if ext_guess:
            for name, exts, _ in shutil.get_unpack_formats():
                if ext_guess in exts:
                    return name

    filename = os.path.normcase(filename)
    for name, exts, _ in shutil.get_unpack_formats():
        for ext in exts:
            if filename.endswith(ext):
                return name

    return None
