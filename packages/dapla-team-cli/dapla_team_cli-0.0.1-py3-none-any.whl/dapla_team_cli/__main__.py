"""Command-line interface.

CLI commands are generally structured according to this convention:
<root> <command-group> <command>

Example:
    Given the command ´dpteam tf iam-bindings´ then...
    ´dpteam´ is the root (CLI name)
    ´tf´ is the command group and
    ´iam-bindings´ is the actual command

Command groups must be mounted here to become available.

Each sub-command's modules should be grouped into a separate python package.
"""
import click

from dapla_team_cli.doctor import doctor
from dapla_team_cli.gcp import gcp
from dapla_team_cli.groups import groups
from dapla_team_cli.tf import tf


@click.group()
@click.version_option()
def main() -> None:
    """Dapla Team CLI root command (dpteam)."""
    pass


main.add_command(tf)
main.add_command(groups)
main.add_command(doctor)
main.add_command(gcp)


if __name__ == "__main__":
    main(prog_name="dpteam")  # pragma: no cover
