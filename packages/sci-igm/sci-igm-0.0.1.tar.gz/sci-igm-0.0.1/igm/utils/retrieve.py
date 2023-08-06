import contextlib
import os
import shutil
import tempfile
import warnings
import weakref
from urllib.request import urlretrieve

import validators
from hbutils.system import copy
from hbutils.testing import vpython
from tqdm import tqdm

from . import get_archive_type
from .archive import unpack_archive
from .path import _samepath
from .tqdm import tqdm_ncols
from .url import get_url_filename
from .vcs import is_vcs_url, retrieve_from_vcs

if vpython >= '3.8':
    LocalTemporaryDirectory = tempfile.TemporaryDirectory
else:
    class LocalTemporaryDirectory(object):  # pragma: no cover
        """
        THIS CLASS IS COPIED FROM PYTHON3.8's TEMPFILE.
        Because PermissionError will be raised when use native TemporaryDirectory on Windows python3.7.
        This class should be removed when python3.7 is no longer supported.

        Create and return a temporary directory.  This has the same
        behavior as mkdtemp but can be used as a context manager.  For
        example:

            with TemporaryDirectory() as tmpdir:
                ...

        Upon exiting the context, the directory and everything contained
        in it are removed.
        """

        def __init__(self, suffix=None, prefix=None, dir=None):
            self.name = tempfile.mkdtemp(suffix, prefix, dir)
            self._finalizer = weakref.finalize(
                self, self._cleanup, self.name,
                warn_message="Implicitly cleaning up {!r}".format(self))

        @classmethod
        def _rmtree(cls, name):
            def onerror(func, path, exc_info):
                if issubclass(exc_info[0], PermissionError):
                    def resetperms(path):
                        try:
                            os.chflags(path, 0)
                        except AttributeError:
                            pass
                        os.chmod(path, 0o700)

                    try:
                        if path != name:
                            resetperms(os.path.dirname(path))
                        resetperms(path)

                        try:
                            os.unlink(path)
                        # PermissionError is raised on FreeBSD for directories
                        except (IsADirectoryError, PermissionError):
                            cls._rmtree(path)
                    except FileNotFoundError:
                        pass
                elif issubclass(exc_info[0], FileNotFoundError):
                    pass
                else:
                    raise

            shutil.rmtree(name, onerror=onerror)

        @classmethod
        def _cleanup(cls, name, warn_message):
            cls._rmtree(name)
            warnings.warn(warn_message, ResourceWarning)

        def __repr__(self):
            return "<{} {!r}>".format(self.__class__.__name__, self.name)

        def __enter__(self):
            return self.name

        def __exit__(self, exc, value, tb):
            self.cleanup()

        def cleanup(self):
            if self._finalizer.detach():
                self._rmtree(self.name)


class TqdmForURLDownload(tqdm):
    """
    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.
    This is the example from tqdm official.
    """

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize


def retrieve_to_local(srcpos, dstpath, auto_unpack: bool = True, silent: bool = False) -> str:
    if is_vcs_url(srcpos):
        if not silent:
            print(f'Cloning from VCS {srcpos!r}...')

        return retrieve_from_vcs(srcpos, dstpath)
    else:
        if validators.url(srcpos):  # is url, need download
            filename = get_url_filename(srcpos)
            with LocalTemporaryDirectory() as tdir:
                if not silent:
                    print(f'Downloading {srcpos!r}...')
                    with TqdmForURLDownload(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                                            ncols=tqdm_ncols()) as t:
                        local_filename, headers = urlretrieve(
                            srcpos, os.path.join(tdir, filename), reporthook=t.update_to, data=None)
                        t.total = t.n
                else:
                    local_filename, headers = urlretrieve(srcpos, os.path.join(tdir, filename))

                archive_format = get_archive_type(filename, headers.get('Content-Type', None))
                if auto_unpack and archive_format:  # unpack archive file to directory
                    if not silent:
                        print(f'Unpacking archive {filename!r}...')

                    unpack_archive(local_filename, dstpath, archive_format)
                    return dstpath
                else:  # just copy the file
                    if not _samepath(local_filename, dstpath):
                        copy(local_filename, dstpath)
                    return dstpath

        else:  # is a local file
            filedir, filename = os.path.split(dstpath)
            archive_format = get_archive_type(filename)
            if auto_unpack and archive_format and os.path.isfile(srcpos):  # is an archive file
                if not silent:
                    print(f'Unpacking archive {filename!r}...')

                unpack_archive(srcpos, dstpath, archive_format)
                return dstpath
            else:  # just copy the file
                if not _samepath(srcpos, dstpath):
                    copy(srcpos, dstpath)
                return dstpath


@contextlib.contextmanager
def retrieve(srcpos, auto_unpack: bool = True, silent: bool = False) -> str:
    with LocalTemporaryDirectory() as td:
        if os.path.exists(srcpos):
            srcpos = os.path.normcase(os.path.normpath(os.path.abspath(srcpos)))
        target = os.path.join(td, get_url_filename(srcpos))
        downloaded = retrieve_to_local(srcpos, target, auto_unpack=auto_unpack, silent=silent)
        yield os.path.join(downloaded)
