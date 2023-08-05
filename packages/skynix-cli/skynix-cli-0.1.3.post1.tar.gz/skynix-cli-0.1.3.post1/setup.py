# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skynix_cli']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['skynix-cli = skynix_cli.skynixcli:cli']}

setup_kwargs = {
    'name': 'skynix-cli',
    'version': '0.1.3.post1',
    'description': '',
    'long_description': '',
    'author': 'AbdelrhmanNile',
    'author_email': 'abdelrhmannile@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
