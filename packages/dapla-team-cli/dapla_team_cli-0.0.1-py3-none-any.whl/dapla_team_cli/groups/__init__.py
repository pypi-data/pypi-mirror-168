"""Groups related commands.

Commands invoked by dpteam groups <some-command> is defined here.
"""

import click

from dapla_team_cli.groups.add_members.cmd import add_members
from dapla_team_cli.groups.list_members.cmd import list_members


@click.group()
def groups() -> None:
    """Groups command group."""
    pass


groups.add_command(add_members)
groups.add_command(list_members)
