import builtins
import os
import warnings
from functools import partial
from typing import List, Dict, Any, Optional, Mapping

from hbutils.system import copy, is_binary_file
from jinja2 import Environment
from potc import transobj as _potc_transobj
from potc.fixture.imports import ImportStatement

from .archive import ArchiveUnpackJob
from .base import RenderJob, DirectoryBasedTask
from .imports import PyImport
from .script import ScriptJob
from ..utils import get_archive_type, splitext


class NotTemplateFile(Exception):
    pass


class IGMRenderTask(DirectoryBasedTask):
    def __init__(self, srcdir: str, dstdir: str, extras: Optional[Mapping[str, Any]] = None):
        DirectoryBasedTask.__init__(self, srcdir, dstdir, extras)

    def _load_job_by_file(self, relfile: str):
        directory, filename = os.path.split(os.path.normcase(relfile))
        if filename.startswith('.') and filename.endswith('.py'):  # script file or template
            if filename.startswith('..'):  # ..xxx.py --> .xxx.py (template)
                return get_common_job(
                    os.path.join(self.srcdir, relfile),
                    os.path.join(self.dstdir, directory, filename[1:]),
                    self._extras
                )
            else:  # .xxx.py --> xxx (script)
                body, _ = splitext(filename)
                return ScriptJob(
                    os.path.join(self.srcdir, relfile),
                    os.path.join(self.dstdir, directory, body[1:]),
                    self._extras
                )
        elif filename.startswith('.') and get_archive_type(filename):  # unpack archive file
            body, _ = splitext(filename)
            return ArchiveUnpackJob(  # .xxx.zip --> xxx (unzip)
                os.path.join(self.srcdir, relfile),
                os.path.join(self.dstdir, directory, body[1:]),
                self._extras
            )
        else:  # common cases
            return get_common_job(  # xxx.yy --> xxx.yy (template/binary copy)
                os.path.join(self.srcdir, relfile),
                os.path.join(self.dstdir, relfile),
                self._extras
            )

    def _yield_jobs(self):
        for curdir, subdirs, files in os.walk(self.srcdir):
            cur_reldir = os.path.relpath(curdir, self.srcdir)
            for file in files:
                curfile = os.path.join(cur_reldir, file)
                try:
                    yield self._load_job_by_file(curfile)
                except NotTemplateFile:  # pragma: no cover
                    pass


def get_common_job(src, dst, extras):
    if is_binary_file(src):
        return CopyJob(src, dst, extras)
    else:
        return TemplateJob(src, dst, extras)


class TemplateImportWarning(Warning):
    pass


class TemplateJob(RenderJob):
    def __init__(self, srcpath: str, dstpath: str, extras: Optional[Mapping[str, Any]] = None):
        RenderJob.__init__(self, srcpath, dstpath)
        self._imps: List[ImportStatement] = []
        self._builtins = {name: getattr(builtins, name) for name in dir(builtins) if not (name.startswith('_'))}
        self._extras = dict(extras or {})
        self._environ = self._create_environ()

    def _yield_extra_funcs(self):
        for name, func in self._extras.items():
            if callable(func):
                yield name, func

    def _create_environ(self):
        environ = Environment(autoescape=False)
        for name, value in self._builtins.items():
            # register function filters
            if 'a' <= name[0] <= 'z' and name not in environ.filters:
                environ.filters[name] = value

            # register type tests
            if 'a' <= name[0] <= 'z' and isinstance(value, type) and name not in environ.tests:
                environ.tests[name] = partial(lambda y, x: isinstance(x, y), value)

        environ.filters['potc'] = self._transobj
        environ.tests['None'] = lambda x: x is None

        for name, func in self._yield_extra_funcs():
            environ.filters[name] = func
            environ.tests[name] = func

        return environ

    def _imports(self) -> List[str]:
        return sorted(map(str, self._imps))

    def _transobj(self, x) -> str:
        result = _potc_transobj(x)
        if result.imports:
            for _import in result.imports:
                self._imps.append(_import)

        return result.code

    def _parameters(self) -> Dict[str, Any]:
        from igm.env import sys, env, user
        return {
            **self._builtins,
            **self._extras,
            'sys': sys, 'env': env, 'user': user,
            'potc': self._transobj, 'py': PyImport(),
        }

    def _run(self):
        with open(self.srcpath, 'r') as rf:
            template = self._environ.from_string(rf.read())

        dstdir, _ = os.path.split(self.dstpath)
        if dstdir:
            os.makedirs(dstdir, exist_ok=True)
        with open(self.dstpath, 'w+') as wf:
            result = template.render(**self._parameters())
            wf.write(result)

        unimports = []
        for imp in self._imports():
            if imp not in result:
                unimports.append(imp)

        if unimports:
            warnings.warn(TemplateImportWarning(
                f'These import statement is suggested to added in template {self.srcpath!r}:{os.linesep}'
                f'{os.linesep.join(unimports)}'
            ))


class CopyJob(RenderJob):
    def __init__(self, srcpath: str, dstpath: str, extras: Optional[Mapping[str, Any]] = None):
        RenderJob.__init__(self, srcpath, dstpath)
        _ = extras

    def _run(self):
        dstdir, _ = os.path.split(self.dstpath)
        if dstdir:
            os.makedirs(dstdir, exist_ok=True)

        copy(self.srcpath, self.dstpath)
