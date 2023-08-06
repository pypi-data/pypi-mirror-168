"""The Add Members CLI Module."""

from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape


jinja_env = Environment(loader=PackageLoader("dapla_team_cli.groups.add_members"), autoescape=select_autoescape())
