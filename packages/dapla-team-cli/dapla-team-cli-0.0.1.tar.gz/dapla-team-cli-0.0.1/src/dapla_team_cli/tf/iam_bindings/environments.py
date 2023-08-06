"""Functionality related to querying the user for GCP envionments."""
from typing import Any

import questionary as q


def ask_for_environments() -> Any:
    """Ask the user for GCP environments the IAM bindings should be applied to.

    One of: `staging`, `prod`
    """
    return q.checkbox(
        message="Environments",
        qmark="🌳",
        choices=[q.Choice("staging", checked=True), q.Choice("prod")],
    ).ask()
