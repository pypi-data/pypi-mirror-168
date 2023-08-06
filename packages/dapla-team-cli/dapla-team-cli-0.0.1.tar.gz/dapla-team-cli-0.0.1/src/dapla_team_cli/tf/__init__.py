"""Terraform related commands.

Commands invoked by ´dpteam tf <some-command>` is defined here.
"""
import click

from dapla_team_cli.tf.iam_bindings.cmd import iam_bindings


@click.group()
def tf() -> None:
    """Terraform command group."""
    pass


tf.add_command(iam_bindings)
