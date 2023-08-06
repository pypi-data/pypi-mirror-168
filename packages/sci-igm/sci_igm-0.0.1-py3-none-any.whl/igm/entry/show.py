import click

from .base import CONTEXT_SETTINGS, command_wrap, ClickErrorException
from ..conf import load_igm_setup
from ..conf.project import load_igm_project, NotIGMProject


class NotIGMTemplateOrProject(ClickErrorException):
    exit_code = 0x20

    def __init__(self, directory):
        ClickErrorException.__init__(self, f'Directory {directory!r} is not an IGM template or project.')


def _show_cli(cli: click.Group):
    @cli.command('show', help='Show meta information of IGM Template.',
                 context_settings=CONTEXT_SETTINGS)
    @click.option('--silent', is_flag=True, default=False,
                  help='Do not show the process of template loading.', show_default=True)
    @click.argument('direct', type=str, default='.')
    @command_wrap()
    def _show(direct: str, silent: bool):
        try:
            with load_igm_setup(direct, silent=silent) as t:  # a template
                click.secho(f'Template: ', nl=False)
                click.secho(t.name, fg='cyan', underline=True)

                click.secho(f'Version: ', nl=False)
                click.secho(t.version, fg='cyan', underline=True)

                if t.description:
                    click.secho(f'Description: ', nl=False)
                    click.secho(t.description, underline=True)
        except FileNotFoundError:  # not a template
            try:
                with load_igm_project(direct) as p:
                    click.secho(f'Name: ', nl=False)
                    click.secho(p.name, fg='blue', underline=True)

                    click.secho(f'Version: ', nl=False)
                    click.secho(p.version, fg='blue', underline=True)

                    click.secho(f'Template Name: ', nl=False)
                    click.secho(p.template_name, fg='cyan', underline=True)

                    click.secho(f'Template Version: ', nl=False)
                    click.secho(p.template_version, fg='cyan', underline=True)

                    click.secho(f'Created at: ', nl=False)
                    click.secho(p.created_at_repr, underline=True)

            except (FileNotFoundError, NotIGMProject):
                raise NotIGMTemplateOrProject(direct)

    return cli
