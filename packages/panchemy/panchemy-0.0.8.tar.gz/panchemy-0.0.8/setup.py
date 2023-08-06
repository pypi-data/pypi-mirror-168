# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.39,<2.0.0', 'pandas>=1.4.3,<2.0.0']

setup_kwargs = {
    'name': 'panchemy',
    'version': '0.0.8',
    'description': 'A library for data handler between SQLAlchemy and pandas',
    'long_description': '',
    'author': 'Alan Nguyen',
    'author_email': 'nnlan.dev.98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NLanN/panchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
