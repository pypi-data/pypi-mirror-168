import builtins
import os
from functools import partial
from typing import Optional, Callable, Mapping, Any

from hbutils.reflection import mount_pythonpath
from hbutils.system import remove

from .inquire import with_user_inquire, inquire_call
from ..render import IGMRenderTask
from ..utils import normpath

_DEFAULT_TEMPLATE_DIR = 'template'


class IGMTemplate:
    def __init__(self, name, version, description,
                 path, template_dir=_DEFAULT_TEMPLATE_DIR,
                 inquire: Optional[Callable[[], Mapping]] = None,
                 extras: Optional[Mapping[str, Any]] = None):
        self.__name = name
        self.__version = version
        self.__description = description

        self.__path = normpath(path)
        self.__template_dir = normpath(self.__path, template_dir)

        self.__inquire = (inquire or (lambda: {}))
        self.__extras = dict(extras or {})

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    @property
    def description(self) -> str:
        return self.__description

    @property
    def path(self) -> str:
        return self.__path

    @property
    def template_dir(self) -> str:
        return self.__template_dir

    def print_info(self, file=None):
        # print is replaced here to print all the output to ``file``
        if file is not None:
            # noinspection PyShadowingBuiltins
            print = partial(builtins.print, file=file)
        else:
            # noinspection PyShadowingBuiltins
            print = builtins.print

        print(f'{self.__name}, v{self.__version}')
        print(f'{self.__description}')
        print(f'Located at {self.__path!r}.')

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self.__name}, v{self.__version}>'

    def run(self, dstdir: str, silent: bool = False) -> bool:
        if os.path.exists(dstdir):
            raise FileExistsError(f'Path {dstdir!r} already exist.')

        ok, inquire_data = inquire_call(self.__inquire)
        if ok:
            try:
                with with_user_inquire(inquire_data), mount_pythonpath(self.__path):
                    task = IGMRenderTask(
                        self.__template_dir, dstdir,
                        {
                            'template': self,
                            'project_dir': os.path.abspath(dstdir),
                            **self.__extras
                        }
                    )
                    task.run(silent=silent)
                return True
            except BaseException:
                if os.path.exists(dstdir):
                    remove(dstdir)
                raise

        else:
            return False
