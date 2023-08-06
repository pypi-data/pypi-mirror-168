"""Groups CLI command definition."""
from typing import Any
from typing import Dict
from typing import List

import click
import questionary as q
import requests

from dapla_team_cli import prompt_custom_style
from dapla_team_cli.config import DAPLA_TEAM_API_BASE
from dapla_team_cli.groups.services.list_groups import deduce_team_info
from dapla_team_cli.tf.iam_bindings import MissingUserSuppliedInfoError
from dapla_team_cli.tf.iam_bindings.auth_groups import AuthGroupValidator
from dapla_team_cli.tf.iam_bindings.cmd import ask_for_team_repo


@click.command()
@click.option(
    "team_name",
    "--team-name",
    "-tn",
    help="Name: Dapla team name, such as `demo-enhjoern-a´",
)
@click.option(
    "group_name",
    "--group-name",
    "-tn",
    help="Name: Dapla team name, such as `demo-enhjoern-a´",
)
def add_members(team_name: str, group_name: str) -> None:
    """Adds new member(s) to the provided auth group.

    Args:
        team_name: The name of the dapla team.
        group_name: Name of the auth group that the member(s) should be added to.

    Raises:
        MissingUserSuppliedInfoError: If team info or group name is not supplied and can not be deduced from current directory.

    """
    print("What auth group would you like to add new members to?")

    if not team_name:
        team = deduce_team_info()
        team_name = team.name
        if not team_name:

            team_name = ask_for_team_repo()
            team_name = team_name.split("/")[-1]

    if not team_name:
        raise MissingUserSuppliedInfoError("Not a IaC repo and no team_name supplied, nothing to do...")

    if not group_name:
        group_name = _ask_for_auth_group(team_name)

    if not group_name:
        raise MissingUserSuppliedInfoError("No Groups were provided, could not complete request...")

    print("Who would you like to add?")

    members = _ask_for_members()

    api_endpoint = DAPLA_TEAM_API_BASE + f"teams/{team_name}/groups/{group_name}"

    payload = {"users": []}  # type: Dict[str, List[Any]]
    for member in members:
        payload["users"].append({"email_short": f"{member}"})

    response = requests.patch(api_endpoint, payload)

    print(response)


def _ask_for_members() -> List[str]:
    """Ask for which members to add to a group. Members consist of all SSB employees.

    Returns:
        Returns a set of members to add.
    """
    api_endpoint = DAPLA_TEAM_API_BASE + "users"
    response = requests.get(api_endpoint).json()

    data = response["_embedded"]["userList"]

    choices = [f'{item["name"]} - {item["emailShort"]}' for item in data]
    meta_information = {}

    for item in data:

        meta_information[f"{item}"] = f"{item['name']} - {item['email']}"

    q.print("(hit enter when done)")
    members_set = set()
    while True:
        member_short_email = q.autocomplete(
            message="Member name",
            choices=choices,
            meta_information=meta_information,
            style=prompt_custom_style,
        ).ask()
        if member_short_email:

            member_short_email = member_short_email.split("-")[1].strip()
            members_set.add(member_short_email)
        else:
            break

    return list(members_set)


def _ask_for_auth_group(team_name: str) -> str:
    """Ask user for the auth group that the new members should be added to.

    Args:
        team_name: The name of the dapla team.

    Returns:
        The auth group the members should be added to.
    """
    auth_group = q.select(
        message="Auth Group",
        instruction="(name of the Auth group the members should be added to)",
        qmark="👥",
        choices=[
            q.Choice(auth_group, value=auth_group)
            for auth_group in [
                f"{team_name}-support",
                f"{team_name}-developers",
                f"{team_name}-data-admins",
                f"{team_name}-managers",
                "Other...",
            ]
        ],
    ).ask()

    if auth_group == "Other...":
        auth_group = q.text(
            message="Custom Auth Group",
            validate=AuthGroupValidator,
        ).ask()

    return str(auth_group)
