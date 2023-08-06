import os
import shutil
from typing import Optional, Mapping, Any

from .base import RenderJob
from ..utils import get_archive_type


class ArchiveUnpackJob(RenderJob):
    def __init__(self, srcpath: str, dstpath: str, extras: Optional[Mapping[str, Any]] = None):
        RenderJob.__init__(self, srcpath, dstpath)
        _ = extras

    def _run(self):
        archive_fmt = get_archive_type(self.srcpath)
        os.makedirs(self.dstpath, exist_ok=True)
        shutil.unpack_archive(self.srcpath, self.dstpath, archive_fmt)
