# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benchling_cli', 'benchling_cli.apps', 'benchling_cli.apps.codegen']

package_data = \
{'': ['*'], 'benchling_cli.apps.codegen': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'autoflake>=1.4,<2.0',
 'benchling_sdk>=1.5.0a0,<2.0.0',
 'black>=22.3.0,<23.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['benchling-cli = benchling_cli.cli:cli']}

setup_kwargs = {
    'name': 'benchling-cli',
    'version': '0.3.0a0',
    'description': 'CLI for assistance in developing with the Benchling Platform.',
    'long_description': 'Benchling CLI\n-------------\n\nA Python 3.8+ CLI for the [Benchling](https://www.benchling.com/) platform designed to assist in developing against the\nBenchling platform\n\nTo see all commands available in the CLI, use `benchling-cli --help`',
    'author': 'Benchling Support',
    'author_email': 'support@benchling.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
