# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dapla_team_cli',
 'dapla_team_cli.doctor',
 'dapla_team_cli.gcp',
 'dapla_team_cli.gcp.add_secret',
 'dapla_team_cli.groups',
 'dapla_team_cli.groups.add_members',
 'dapla_team_cli.groups.list_members',
 'dapla_team_cli.groups.services',
 'dapla_team_cli.tf',
 'dapla_team_cli.tf.iam_bindings']

package_data = \
{'': ['*'],
 'dapla_team_cli.groups.add_members': ['templates/*'],
 'dapla_team_cli.tf.iam_bindings': ['templates/*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'azure-cli>=2.40.0,<3.0.0',
 'click>=8.1.3',
 'devtools>=0.9.0,<0.10.0',
 'google-cloud-secret-manager>=2.12.4,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-tfvars>=0.1.0,<0.2.0',
 'questionary>=1.10.0,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'twine>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['dpteam = dapla_team_cli.__main__:main']}

setup_kwargs = {
    'name': 'dapla-team-cli',
    'version': '0.0.1',
    'description': 'CLI for working with Dapla Teams',
    'long_description': '# Dapla Team CLI\n\n[![PyPI](https://img.shields.io/pypi/v/dapla-team-cli.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/dapla-team-cli.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/dapla-team-cli)][python version]\n[![License](https://img.shields.io/pypi/l/dapla-team-cli)][license]\n\n[![Tests](https://github.com/statisticsnorway/dapla-team-cli/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/statisticsnorway/dapla-team-cli/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/dapla-team-cli/\n[status]: https://pypi.org/project/dapla-team-cli/\n[python version]: https://pypi.org/project/dapla-team-cli\n[tests]: https://github.com/statisticsnorway/dapla-team-cli/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/statisticsnorway/dapla-team-cli\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nA CLI for working with Dapla teams.\n\n![IAM Bindings](docs/iam-bindings.gif)\n\n## Features\n\n- Generate IAM Bindings\n\n## Installation\n\nYou can install _Dapla Team CLI_ via [pipx] from [PyPI]:\n\n```console\n$ pipx install dapla-team-cli\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Dapla Team CLI_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n[pypi]: https://pypi.org/\n[file an issue]: https://github.com/statisticsnorway/dapla-team-cli/issues\n[pipx]: https://pypa.github.io/pipx\n\n<!-- github-only -->\n\n[license]: https://github.com/statisticsnorway/dapla-team-cli/blob/main/LICENSE\n[contributor guide]: https://github.com/statisticsnorway/dapla-team-cli/blob/main/CONTRIBUTING.md\n[command-line reference]: https://github.io/statisticsnorway/dapla-team-cli/usage.html\n',
    'author': 'Kenneth Leine Schulstad',
    'author_email': 'kls@rdck.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/statisticsnorway/dapla-team-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
