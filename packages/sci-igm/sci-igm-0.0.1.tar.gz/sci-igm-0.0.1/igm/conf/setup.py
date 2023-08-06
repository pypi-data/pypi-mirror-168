import contextlib
import inspect
import os
from typing import Dict, ContextManager, Optional, Callable, Mapping, Any

from hbutils.random import random_sha1_with_timestamp
from hbutils.reflection import mount_pythonpath
from hbutils.testing import disable_output

from .requirement import load_req, check_req, pip
from .template import IGMTemplate, _DEFAULT_TEMPLATE_DIR
from ..utils import get_global_env, retrieve, normpath

_IGM_SESSIONS: Dict[str, IGMTemplate] = {}
_IGM_SESSION_ID_NAME = '__igm_session_id__'
_IGM_PATH_NAME = '__igm_path__'

_DEFAULT_REQ_FILE = 'requirements.txt'


def igm_setup(
        *,
        name: str,
        version: str,
        description: str,
        template_dir: str = _DEFAULT_TEMPLATE_DIR,
        inquire: Optional[Callable[[], Mapping]] = None,
        extras: Optional[Mapping[str, Any]] = None
) -> IGMTemplate:
    outer_frame = inspect.currentframe().f_back
    outer_dir, _ = os.path.split(os.path.abspath(outer_frame.f_code.co_filename))

    session_id = get_global_env(_IGM_SESSION_ID_NAME, default=None)
    path = get_global_env(_IGM_PATH_NAME, default=outer_dir)

    retval = IGMTemplate(
        # meta information
        name, version, description,

        # directory configuration
        path=path,
        template_dir=template_dir,

        # inquire
        inquire=inquire,
        extras=extras,
    )
    if session_id is not None:
        _IGM_SESSIONS[session_id] = retval

    return retval


@contextlib.contextmanager
def load_igm_setup(template: str, *segment: str,
                   setup_filename='meta.py', silent: bool = False) -> ContextManager[IGMTemplate]:
    with retrieve(template, silent=silent) as path:
        path = os.path.abspath(os.path.join(path, *segment))
        pathdir, pathfile = path, os.path.join(path, setup_filename)

        session_id = random_sha1_with_timestamp()
        with mount_pythonpath(pathdir):
            # install requirements
            _reqfile = normpath(pathdir, _DEFAULT_REQ_FILE)
            if os.path.exists(_reqfile):
                requirements = load_req(_reqfile)
                if not check_req(requirements):
                    args = ['install', *requirements]
                    if silent:
                        with disable_output():
                            pip(*args)
                    else:
                        pip(*args)

            # load source file
            with open(pathfile, 'r') as sf:
                exec(sf.read(), {
                    _IGM_SESSION_ID_NAME: session_id,
                    _IGM_PATH_NAME: pathdir,
                })

            assert session_id in _IGM_SESSIONS, f'Session {session_id!r} not found.'
            yield _IGM_SESSIONS[session_id]
