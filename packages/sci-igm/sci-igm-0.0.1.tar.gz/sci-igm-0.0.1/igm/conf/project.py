import builtins
import datetime
import os.path
import shlex
import subprocess
import sys
from contextlib import contextmanager
from functools import partial
from typing import Union, List, Any, Mapping, Optional, ContextManager, Dict

from hbutils.reflection import mount_pythonpath
from hbutils.string import plural_word

from ..utils import get_globals


class IGMScript:
    def describe(self) -> str:
        raise NotImplementedError  # pragma: no cover

    def run(self, pfunc=None):
        self._run_with_wrapper(pfunc)

    def _run_with_wrapper(self, pfunc=None, prefix=None):
        pfunc = pfunc or partial(builtins.print, flush=True)
        title = self.describe() if not prefix else f'{prefix} {self.describe()}'
        pfunc(title)
        self._run()

    def _run(self):
        raise NotImplementedError  # pragma: no cover


class IGMFuncScript(IGMScript):
    def __init__(self, func):
        self.func = func

    def describe(self) -> str:
        if getattr(self.func, '__doc__', None) and self.func.__doc__.strip():
            return self.func.__doc__.strip()
        else:
            return f'Call function {self.func.__name__!r}.'

    def _run(self):
        self.func()


def _trans_command(command: Union[List[str], str]) -> List[str]:
    if isinstance(command, str):
        return shlex.split(command)
    else:
        return command


def _repr_command(command: Union[List[str], str]) -> str:
    return ' '.join(map(shlex.quote, _trans_command(command)))


class IGMCommandScript(IGMScript):
    def __init__(self, command: Union[List[str], str]):
        self.args = _trans_command(command)

    def _visual_command(self) -> List[str]:
        return self.args

    def describe(self) -> str:
        return f'Command - {_repr_command(self._visual_command())}'

    def _run(self):
        process = subprocess.run(self.args, stdin=sys.stdin, stderr=sys.stderr, stdout=sys.stdout)
        process.check_returncode()


class IGMPythonScript(IGMCommandScript):
    def __init__(self, command: Union[List[str], str]):
        self._python_command = _trans_command(command)
        IGMCommandScript.__init__(self, [sys.executable, *self._python_command])

    def _visual_command(self) -> List[str]:
        return ['python', *self._python_command]


class IGMPipScript(IGMPythonScript):
    def __init__(self, command: Union[List[str], str]):
        self._pip_command = _trans_command(command)
        IGMPythonScript.__init__(self, ['-m', 'pip', *self._pip_command])

    def _visual_command(self) -> List[str]:
        return ['pip', *self._pip_command]


class IGMScriptSet(IGMScript):
    def __init__(self, *scripts: 'IGMScript', desc: Optional[str] = None):
        self.scripts = scripts
        self.desc = desc

    def describe(self) -> str:
        return self.desc or f'Run a set of {plural_word(len(self.scripts), "scripts")} in order.'

    def _run_with_wrapper(self, pfunc=None, prefix=None):
        pfunc = pfunc or partial(builtins.print, flush=True)
        title = self.describe() if not prefix else f'{prefix} {self.describe()}'
        pfunc(title)
        try:
            for i, script in enumerate(self.scripts, start=1):
                new_prefix = f'{prefix}{i}.' if prefix else f'{i}.'
                script._run_with_wrapper(pfunc, new_prefix)
        finally:
            print(flush=True)

    def _run(self):
        raise NotImplementedError  # pragma: no cover


def _to_script(v):
    if isinstance(v, IGMScript):
        return v
    elif isinstance(v, str):
        return IGMCommandScript(v)
    elif callable(v):
        return IGMFuncScript(v)
    elif isinstance(v, (list, tuple)):
        if all([isinstance(x, str) for x in v]):
            return IGMCommandScript(v)
        else:
            return IGMScriptSet(*map(_to_script, v))
    else:  # pragma: no cover
        raise TypeError(f'Unknown script type - {v!r}.')


def cpy(command: Union[List[str], str], *cmd: str) -> IGMPythonScript:
    return IGMPythonScript([command, *cmd] if cmd else command)


def cpip(command: Union[List[str], str], *cmd: str) -> IGMPipScript:
    return IGMPipScript([command, *cmd] if cmd else command)


def cmds(description: str, v: List) -> IGMScriptSet:
    return IGMScriptSet(*map(_to_script, v), desc=description)


def _to_timestamp(v) -> float:
    if isinstance(v, str):
        return datetime.datetime.fromisoformat(v).timestamp()
    elif isinstance(v, (int, float)):
        return float(v)
    else:
        raise TypeError(f'Invalid time type - {v!r}.')


def _timestamp_repr(v) -> str:
    _local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    return datetime.datetime.fromtimestamp(_to_timestamp(v), _local_timezone).isoformat()


class IGMProject:
    def __init__(self, name, version, template_name, template_version, created_at, params, scripts):
        self.name = name
        self.version = version
        self.template_name = template_name
        self.template_version = template_version
        self.created_at = _to_timestamp(created_at)
        self.params = dict(params or {})
        self.scripts: Dict[Optional[str], IGMScript] = \
            {name: _to_script(s) for name, s in (scripts or {}).items()}

    @property
    def created_at_repr(self) -> str:
        return _timestamp_repr(self.created_at)


_IGM_PROJECT_TAG = '__igm_project__'


def igm_project(
        name,
        version,
        template_name,
        template_version,
        created_at,
        params: Optional[Mapping[str, Any]] = None,
        scripts: Optional[Mapping[Optional[str], Any]] = None,
):
    g = get_globals()
    proj = IGMProject(
        name, version,
        template_name, template_version, created_at,
        params, scripts,
    )

    g[_IGM_PROJECT_TAG] = proj
    return proj


class NotIGMProject(Exception):
    pass


@contextmanager
def load_igm_project(directory, meta_filename='igmeta.py') -> ContextManager[IGMProject]:
    if not os.path.exists(directory):
        raise FileNotFoundError(directory)

    if os.path.isfile(directory):
        proj_dir, metafile = os.path.split(os.path.abspath(directory))
    else:
        proj_dir, metafile = os.path.abspath(directory), meta_filename

    _globals = {}
    with mount_pythonpath(proj_dir):
        with open(os.path.join(proj_dir, metafile), 'r') as f:
            exec(f.read(), _globals)

        _project = _globals.get(_IGM_PROJECT_TAG, None)
        if isinstance(_project, IGMProject):
            yield _project
        else:
            raise NotIGMProject(directory)
