import os.path
from collections.abc import Sequence
from contextlib import contextmanager
from typing import Iterable, Optional, Mapping, Any, Iterator

from hbutils.string import plural_word
from hbutils.testing import capture_output
from tqdm import tqdm

from igm.utils import tqdm_ncols


class RenderTask(Sequence):
    def __init__(self, jobs: Iterable['RenderJob']):
        self.__jobs = list(jobs)

    def __len__(self):
        return len(self.__jobs)

    def __getitem__(self, index):
        return self.__jobs[index]

    def run(self, silent: bool = False):
        raise NotImplementedError  # pragma: no cover


class DirectoryBasedTask(RenderTask):
    def __init__(self, srcdir: str, dstdir: str, extras: Optional[Mapping[str, Any]] = None):
        self.srcdir = srcdir
        self.dstdir = dstdir
        self._extras = dict(extras or {})
        RenderTask.__init__(self, list(self._yield_jobs()))

    def _yield_jobs(self) -> Iterator['RenderJob']:
        raise NotImplementedError  # pragma: no cover

    def run(self, silent: bool = False):
        # initialize
        if not silent:
            jobs = tqdm(self, ncols=tqdm_ncols(), leave=True)
            pgbar = jobs
        else:
            jobs = self
            pgbar = None

        os.makedirs(self.dstdir, exist_ok=True)
        # run jobs
        for job in jobs:
            if pgbar:
                pgbar.set_description(os.path.relpath(job.srcpath, self.srcdir))
                pgbar.update()
            job.run(silent=silent)

        # run complete
        if pgbar:
            pgbar.set_description('Complete.')
            pgbar.update()

    def __repr__(self):
        return f'<{type(self).__name__} {plural_word(len(self), "job")}, srcdir: {self.srcdir!r}>'


class RenderJob:
    def __init__(self, srcpath, dstpath=None):
        self.srcpath = srcpath
        self.dstpath = dstpath

    def _run(self):
        raise NotImplementedError  # pragma: no cover

    def run(self, silent: bool = False):
        with silent_wrapper(silent):
            return self._run()


@contextmanager
def silent_wrapper(silent):
    """
    Overview:
        A wrapper for silencing the output inside.

    :param silent: Silent or not. If ``True``, the output will be captured and ignored.
    """
    if silent:
        with capture_output():
            yield
    else:
        yield
