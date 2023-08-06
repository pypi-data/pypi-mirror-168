# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['falcon_alliance',
 'falcon_alliance.schemas',
 'falcon_alliance.tests',
 'falcon_alliance.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-client-cache>=0.7.3,<0.8.0',
 'aiohttp>=3.8.1,<3.9.0',
 'coverage>=6.4.4,<6.5.0',
 'pytest>=7.1.2,<7.2.0',
 'python-dotenv>=0.19,<1.0']

setup_kwargs = {
    'name': 'falcon-alliance',
    'version': '0.1.0',
    'description': 'A Pythonic library that attains FRC-related information from sources like The Blue Alliance and more.',
    'long_description': None,
    'author': 'The Falcons - Team 4099',
    'author_email': 'contact@team4099.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
