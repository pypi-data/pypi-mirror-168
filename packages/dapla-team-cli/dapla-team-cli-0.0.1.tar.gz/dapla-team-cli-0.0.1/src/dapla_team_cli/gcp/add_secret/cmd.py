"""List-members CLI command definition."""

import subprocess
from typing import Any

import click
import questionary as q
from google.cloud import secretmanager


@click.command()
@click.option(
    "project_id",
    "--project_id",
    "-pid",
    help="Example: taging-demo-enhjoern-a-6a2d",
)
@click.option(
    "secret_id",
    "--secret_id",
    "-sid",
    help="Example: 8237891769",
)
@click.option(
    "payload",
    "--playload",
    "-p",
    help="The actual secret to be added in secret manager.",
)
def add_secret(project_id: str, secret_id: str, payload: str) -> None:
    """Create a new secret and a new secret version within the provided project.

    Args:
        project_id: The ID of the project that the secret should be created in.
        secret_id: The ID of the secret to be created.
        payload: The payload of the secret to be created.
    """
    if not project_id:
        project_id = q.text("What is the project ID of the project you wish to add a secret to?").ask()
    if not secret_id:
        secret_id = q.text("What should the secret id be?").ask()
    if not payload:
        payload = q.text("What is the secret that should be added?").ask()

    subprocess.run(["gcloud", "auth", "application-default", "login"])

    request_secret_creation(project_id, secret_id)

    add_secret_version(project_id, secret_id, payload)

    print("The secret was successfully created")


def add_secret_version(project_id: str, secret_id: str, payload: Any) -> None:
    """Requests google cloud storage client to create a secret.

    Args:
        project_id: The ID of the project that the secret should be created in.
        secret_id: The ID of the secret to be created.
        payload: The payload of the secret to be created.
    """
    client = secretmanager.SecretManagerServiceClient()

    parent = client.secret_path(project_id, secret_id)

    payload = payload.encode("UTF-8")

    response = client.add_secret_version(
        request={
            "parent": parent,
            "payload": {"data": payload},
        }
    )

    print(f"Added secret version: {response.name}")


def request_secret_creation(project_id: str, secret_id: str) -> None:
    """Requests google cloud storage client to create a secret.

    Args:
        project_id: The ID of the project that the secret should be created in.
        secret_id: The ID of the secret to be created.
    """
    client = secretmanager.SecretManagerServiceClient()

    parent = f"projects/{project_id}"

    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )

    print(f"Created secret: {response.name}")
