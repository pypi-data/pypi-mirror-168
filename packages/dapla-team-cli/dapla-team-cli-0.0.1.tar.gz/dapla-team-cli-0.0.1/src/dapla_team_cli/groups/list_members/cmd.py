"""List-members CLI command definition."""
from typing import List

import click
import requests
from rich.console import Console
from rich.table import Table

from dapla_team_cli.config import DAPLA_TEAM_API_BASE
from dapla_team_cli.groups.list_members.member import Member
from dapla_team_cli.groups.services.list_groups import deduce_team_info
from dapla_team_cli.tf.iam_bindings import MissingUserSuppliedInfoError


@click.command()
@click.option(
    "team_name",
    "--team-name",
    "-tn",
    help="Name: Dapla team name, such as `demo-enhjoern-a´",
)
def list_members(team_name: str) -> None:
    """Lists members for a given Dapla team (e.g. `demo-enhjoern-a`).

    The tool will first look for your team name in .tfvars file in your current working directory,
    you can also specify a team name as a parameter.

    Args:
        team_name: Dapla team name, such as `demo-enhjoern-a`

    Raises:
        MissingUserSuppliedInfoError: if the user failed to specify a team name (e.g. `--team-name
            demo-enhjoern-a`) and the command is called outside a IaC Repo.
    """
    if not team_name:
        team = deduce_team_info()
        team_name = team.name

    if not team_name:
        raise MissingUserSuppliedInfoError("Not a IaC repo and no team_name supplied, nothing to do...")

    api_endpoint = DAPLA_TEAM_API_BASE + f"teams/{team_name}/groups"

    data = requests.get(api_endpoint).json()

    members_list = []
    for group in data["_embedded"]["groupList"]:
        group_name = group["id"]
        for member in group["users"]:
            members_list.append(Member(name=member["name"], email_short=member["emailShort"]))

            _print_table(members_list, group_name)


def _add_row(member: Member, table: Table) -> Table:
    """Adds a Member; name and shortform email to a row in a table.

    Args:
        member: Dapla team member to add
        table: Table to store the new row inn.

    Returns:
        Table used to add more rows or to draw to console
    """
    name = f"[b]{member.name}[/b]"
    table.add_row(f"[b]{name}[/b]", f"[b]{member.email_short}[/b]")
    return table


def _print_table(members: List[Member], team_name: str) -> Table:
    """Makes a table and prints it to console.

    Adds columns for all member attributes, adds team name as title and
    calls _add_row on every member to add rows with member their information.

    Args:
        members: List of Dapla team member to add
        team_name: Dapla team name and auth group combined (e.g. demo-enhjoern-a-support).

    Returns:
        Table, that was used to print
    """
    table = Table(title=f"\n[b]{team_name}[/b]")
    table.add_column("[b]Name[/b]", justify="left")
    table.add_column("[b]Email[/b]", justify="left")
    table.min_width = 100

    for member in members:
        _add_row(member, table)

    console = Console()
    console.print(table)
    return table
