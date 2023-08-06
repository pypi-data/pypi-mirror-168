"""Functionality related to querying the user for bucket access."""
import re
from typing import List
from typing import Optional

import questionary as q
from prompt_toolkit.document import Document
from pydantic import BaseModel


class BucketAuth(BaseModel):
    """A `BucketAuth` references a bucket and holds an associated access type (read or write).

    Attributes:
        simple_name: the name (_without_ the `ssb-<env>-<team-name>` prefix), such as `data-produkt`
        access_type: `read` or `write`
    """

    simple_name: str
    access_type: str


class SimpleBucketNameValidator(q.Validator):
    """Questionary Validator used for checking if a user provided bucket name is properly formatted."""

    def validate(self, document: Document) -> None:
        """Validate that a bucket name is appropriately formatted.

        Args:
            document: The document to validate

        Raises:
             ValidationError: if input does not adhere to the naming convention.
        """
        ok = not document.text or re.match(
            r"^(?!ssb-)(?!staging|prod)[a-z][a-z0-9-]+[a-z0-9]$",
            document.text,
        )
        if not ok:
            raise q.ValidationError(
                message="lowercase letters (a-z), digits or dashes, without ssb or environment prefixes",
                cursor_position=len(document.text),
            )


def ask_for_buckets(team_name: str, auth_group: str) -> List[BucketAuth]:
    """Ask the user for buckets to which access should be granted.

    Also prompt for which environments and until which timestamp the access should be granted.

    The user can select buckets from a list, or supply a custom (other) bucket name.

    Args:
        team_name: The Dapla team name, used for customizing the prompts
        auth_group: The auth group name, used for customizing the prompts

    Returns:
        A list of buckets
    """
    buckets: List[BucketAuth] = []
    other = "other..."

    if not q.confirm(f"Should {auth_group} be authorized to access any buckets?").ask():
        return buckets

    choices = []
    for simple_name in ["data-kilde", "data-produkt", "data-delt"]:
        for access_type in ["read", "write"]:
            choices.append(
                q.Choice(
                    f"ssb-<env>-{team_name}-{simple_name} ({access_type})",
                    value=BucketAuth(simple_name=simple_name, access_type=access_type),
                )
            )
    other_bucket = BucketAuth(simple_name=other, access_type="N/A")
    choices.append(q.Choice("other...", value=other_bucket))

    buckets = q.checkbox(
        message="Buckets",
        qmark="🪣",
        choices=choices,
    ).ask()

    if other_bucket in buckets:
        buckets.remove(other_bucket)
        while True:
            q.print("(hit enter when done)")
            bucket = ask_for_other_bucket(team_name)
            if bucket:
                buckets.append(bucket)
            else:
                break

    return buckets


def ask_for_other_bucket(team_name: str) -> Optional[BucketAuth]:
    """Query for a custom bucket.

    This path is taken if the user selects "other" in the bucket choices dialog.

    Args:
        team_name: The team name. Used for deducing full bucket name.

    Returns:
        A custom bucket name
    """
    simple_name = q.text(
        "Other Bucket",
        validate=SimpleBucketNameValidator,
        instruction=(f"(without the 'ssb-<env>-{team_name}-' prefix)"),
    ).ask()
    if not simple_name:
        return None
    access_type = q.select("Read or Write?", choices=[q.Choice("read"), q.Choice("write")]).ask()

    return BucketAuth(simple_name=simple_name, access_type=access_type)


def filter_buckets(buckets: List[BucketAuth], filter_val: str, env: str, team_name: str) -> List[str]:
    """Filter `buckets` and deduce bucket names from env and `team_name`.

    Args:
        buckets: list of BucketAuths specified by the user
        filter_val: string used for filtering buckets in the buckets list
        env: name of environment
        team_name: name of team

    Returns:
        List of real bucket names filtered by some criteria (such as access_type)

    """
    filter_val = filter_val or ""
    return [f"ssb-{env}-{team_name}-{b.simple_name}" for b in buckets if filter_val in b.simple_name or filter_val in b.access_type]
