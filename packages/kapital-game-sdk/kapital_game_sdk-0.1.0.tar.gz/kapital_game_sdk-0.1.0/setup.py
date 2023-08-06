# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kapital_game_sdk']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'requests>=2.28.1,<3.0.0', 'types-PyYAML>=6.0.11,<7.0.0']

setup_kwargs = {
    'name': 'kapital-game-sdk',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Playground Labs',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
