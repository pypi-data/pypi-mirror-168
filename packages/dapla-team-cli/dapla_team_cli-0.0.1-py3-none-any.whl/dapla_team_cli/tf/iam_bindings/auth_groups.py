"""Auth groups represent a collection of users within a Dapla team.

These groups allow a team to be composed of users with different responsibilities. Each group is associated with roles
and permissions through IAM bindings. The team's administrators can dynamically decide which users should be
member of each auth group - as opposed to granting roles directly to specific users.

Thus, in order for a specific user to be granted a certain role, the user must be a member of the auth group.

Auth groups are named like so:
`<team-name>-<auth-group-simple-name>`

Examples:
    ```
    demo-enhjoern-a-managers
    demo-enhjoern-a-data-admins
    demo-enhjoern-a-developers
    demo-enhjoern-a-consumers
    demo-enhjoern-a-support
    ```

The master system for authorization groups is Active Directory (AD). The groups are automatically mirrored
into GCP as IAM groups.
"""
import re

import questionary as q
from prompt_toolkit.document import Document
from pydantic import BaseModel


class AuthGroup(BaseModel):
    """An `AuthGroup` references a collection of Dapla users.

    Attributes:
        name: the full name of the auth group (_including_ the team name prefix), such as `demo-enhjoern-a-data-admins`
        simple_name: the name (_without_ the team-name prefix), such as `data-admins`
    """

    name: str
    shortname: str


class AuthGroupValidator(q.Validator):
    """Questionary Validator used for checking if the user provided `AuthGroup` is properly formatted."""

    def validate(self, document: Document) -> None:
        """Validate that an AuthGroup is appropriately formatted.

        Args:
            document: The document to validate

        Raises:
             ValidationError: if input does not adhere to the naming convention.
        """
        ok = re.match(
            r"^[a-z][a-z0-9-]+[a-z0-9]$",
            document.text,
        )
        if not ok:
            raise q.ValidationError(
                message="Min 3 lowercase letters (a-z), digits or dashes",
                cursor_position=len(document.text),
            )


def ask_for_auth_group_name(team_name: str) -> str:
    """Ask the user for auth group to use.

    Args:
        team_name: The Dapla team name

    Returns:
        selected auth group name
    """
    auth_group = q.select(
        message="Auth Group",
        instruction="(name of the AD group to configure IAM bindings for)",
        qmark="👥",
        choices=[
            q.Choice(auth_group, value=auth_group)
            for auth_group in [
                f"{team_name}-support",
                f"{team_name}-developers",
                f"{team_name}-data-admins",
                f"{team_name}-managers",
                "other...",
            ]
        ],
    ).ask()

    if auth_group == "other...":
        auth_group = q.text(
            message="Custom Auth Group",
            validate=AuthGroupValidator,
        ).ask()

    return str(auth_group)
