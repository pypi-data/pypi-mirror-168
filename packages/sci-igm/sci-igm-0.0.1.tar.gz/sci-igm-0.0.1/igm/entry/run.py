import os
from contextlib import contextmanager
from typing import ContextManager, Tuple, Optional

import click

from .base import CONTEXT_SETTINGS, command_wrap, ClickWarningException, ClickErrorException
from ..conf.project import load_igm_project, IGMProject, NotIGMProject, IGMScript


@contextmanager
def _current_project() -> ContextManager[Tuple[Optional[str], Optional[IGMProject]]]:
    path, found = os.path.normpath(os.path.abspath(os.curdir)), False
    while True:
        try:
            with load_igm_project(path) as p:
                found = True
                yield path, p
                break
        except (FileNotFoundError, NotIGMProject):
            pass

        newpath = os.path.normpath(os.path.join(path, '..'))
        if path == newpath:
            break
        path = newpath

    if not found:
        yield None, None


class NotIGMProjectHere(ClickErrorException):
    exit_code = 0x30


class NoDefaultScript(ClickWarningException):
    exit_code = 0x31


def title_print(*args):
    click.secho(*args, bold=True, fg='magenta', nl=True)
    click.secho(nl=False)


def no_print(*args):
    _ = args


def script_append(cli: click.Group, name: str, script: IGMScript):
    @cli.command(name, help=script.describe(), context_settings=CONTEXT_SETTINGS)
    @click.option('-L', '--no-label', 'no_label', is_flag=True, default=False,
                  help='Do not show the labels of each step.', show_default=True)
    @command_wrap()
    def _command(no_label: bool):
        with _current_project() as (path, proj):
            os.chdir(path)
            proj.scripts[name].run(title_print if not no_label else no_print)


def _run_cli(cli: click.Group):
    with _current_project() as (_, p):
        if p is None:  # not a project
            @cli.command('run', help='Run script of the IGM project.\n'
                                     '(Not an IGM project here)',
                         context_settings=CONTEXT_SETTINGS)
            @command_wrap()
            def _run():
                raise NotIGMProjectHere('Not an IGM project here.')
        else:
            if None in p.scripts:
                @cli.group('run', help='Run script of the IGM project.\n\n'
                                       f'Default: {p.scripts[None].describe()}',
                           context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
                @click.option('-L', '--no-label', 'no_label', is_flag=True, default=False,
                              help='Do not show the labels of each step.', show_default=True)
                @click.pass_context
                @command_wrap()
                def _run(ctx, no_label: bool):
                    if ctx.invoked_subcommand is None:
                        with _current_project() as (path, proj):
                            os.chdir(path)
                            proj.scripts[None].run(title_print if not no_label else no_print)

            else:
                @cli.group('run', help='Run script of the IGM project.',
                           context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
                @click.pass_context
                @command_wrap()
                def _run(ctx):
                    if ctx.invoked_subcommand is None:
                        raise NoDefaultScript('No default script in this project.\n'
                                              'If you need to assign one, just set its name to \'None\'.')

            rc: click.Group = _run
            for name, script in p.scripts.items():
                if name is None:
                    continue

                script_append(rc, name, script)

    return cli
