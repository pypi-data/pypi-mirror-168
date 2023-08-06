"""Common models and functionality related to Dapla teams members."""
from pydantic import BaseModel


class Member(BaseModel):
    """Information about a Dapla team member.

    Attributes:
        name: Display name from ad, such as `Nordmann, Ola`
        jobb_title: Job title, such as `Konsulent`
        email: Email, such as `noo@ssb.no`
    """

    name: str
    email_short: str


def get_full_name(self: Member) -> str:
    """Get the full name of Member.

    Args:
        self: This members full name.

    Returns:
        Full name of this member.
    """
    return self.name
