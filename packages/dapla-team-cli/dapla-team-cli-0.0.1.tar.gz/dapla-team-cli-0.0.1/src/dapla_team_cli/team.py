"""Common models and functionality related to Dapla teams."""
from pydantic import BaseModel


class TeamInfo(BaseModel):
    """Information about a Dapla team.

    Attributes:
        name: Dapla team name, such as `demo-enhjoern-a`
        iac_repo_path: Path to a local clone of the iac repo
    """

    name: str
    org_nr: str
    iac_repo_path: str
