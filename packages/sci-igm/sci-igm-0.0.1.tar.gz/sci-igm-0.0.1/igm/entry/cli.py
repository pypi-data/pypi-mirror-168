import click

from .dispatch import igm
from .new import _new_cli
from .run import _run_cli
from .show import _show_cli

_DECORATORS = [  # all the sub commands here, using decorator pattern
    _show_cli,
    _new_cli,
    _run_cli,
]


def get_cli_entry() -> click.Group:
    cli = igm
    for deco in _DECORATORS:
        cli = deco(cli)
    return cli


def cli_entry():
    return get_cli_entry()()
