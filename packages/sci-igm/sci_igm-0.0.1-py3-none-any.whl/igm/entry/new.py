import os.path

import click
from click.exceptions import ClickException

from .base import CONTEXT_SETTINGS, ClickWarningException, command_wrap
from ..conf import load_igm_setup


class DestPathAlreadyExist(ClickWarningException):
    exit_code = 0x10

    def __init__(self, dstpath):
        ClickException.__init__(self, f'Path {dstpath!r} already exist, unable to create project.')


class CreationCancelled(ClickWarningException):
    exit_code = 0x11

    def __init__(self):
        ClickException.__init__(self, 'Project creation cancelled.')


def _new_cli(cli: click.Group):
    @cli.command('new', help='Create new AI project from IGM Template.',
                 context_settings=CONTEXT_SETTINGS)
    @click.option('--silent', is_flag=True, default=False,
                  help='Do not show the process of template loading and rendering.', show_default=True)
    @click.argument('template', type=str)
    @click.argument('dst', type=click.Path(exists=False))
    @command_wrap()
    def _new(template, dst, silent: bool):
        if os.path.exists(dst):
            raise DestPathAlreadyExist(dst)

        with load_igm_setup(template, silent=silent) as t:
            created = t.run(dst, silent=silent)

        click.secho()
        if created:
            click.secho(f'New project has been created at {dst!r}.', fg='green')
        else:
            raise CreationCancelled

    return cli
