"""GCP specific stuff."""
import importlib.resources
import json

import click
import questionary as q
from prompt_toolkit.document import Document
from pydantic import BaseModel

from dapla_team_cli.gcp.add_secret.cmd import add_secret


@click.group()
def gcp() -> None:
    """GCP command group."""
    pass


gcp.add_command(add_secret)


with importlib.resources.open_text("dapla_team_cli.gcp", "project_roles.json") as file:
    items = json.load(file)
    gcp_project_roles = {item["name"]: item for item in items}


class GCPRole(BaseModel):
    """A `GCPRole` holds information about a GCP role, such as name and description.

    Args:
        document: The document to validate

    Attributes:
        name: The technical name of the GCP role, such as `roles/bigquery.admin`
        title: A display friendly name, such as `BigQuery Admin`
        description: A descriptive text that gives a short presentation of the role,
            such as ``Administer all BigQuery resources and data
    """

    name: str
    title: str
    description: str


class GCPRoleValidator(q.Validator):
    """Questionary Validator used for checking if the user provided GCP role is properly formatted."""

    def validate(self, document: Document) -> None:
        """Validate that a GCP role name is appropriately formatted.

        Args:
            document: The document to validate

        Raises:
             ValidationError: if input does not adhere to the naming convention.
        """
        ok = not document.text or "roles/" in document.text and document.text in gcp_project_roles.keys()
        if not ok:
            raise q.ValidationError(message="Please choose a GCP Role", cursor_position=len(document.text))
