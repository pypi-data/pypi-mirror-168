"""The IAM Bindings CLI command module."""
from typing import List

from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape
from pydantic import BaseModel

from dapla_team_cli.gcp import GCPRole
from dapla_team_cli.tf.iam_bindings.auth_groups import AuthGroup
from dapla_team_cli.tf.iam_bindings.buckets import BucketAuth
from dapla_team_cli.tf.iam_bindings.expiry import Expiry


jinja_env = Environment(loader=PackageLoader("dapla_team_cli.tf.iam_bindings"), autoescape=select_autoescape())


class IAMBindingConfig(BaseModel):
    """User supplied preferences used for generating IAM Binding Terraform files.

    Attributes:
        team_name: Name of the Dapla team, such as `demo-enhjoern-a`
        auth_group: The selected auth group the IAM bindings should work with
    """

    team_name: str
    auth_group: AuthGroup
    project_roles: List[GCPRole]
    buckets: List[BucketAuth]
    environments: List[str]
    org_nr: str
    gcp_projects: List[str]
    expiry: Expiry


class MissingUserSuppliedInfoError(Exception):
    """Exception that could occur if a user did not supply enough information for a command to execute."""
