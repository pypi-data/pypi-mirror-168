# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite', 'cognite.air']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk>=4.5,<5.0',
 'pandas>=1.1.5,<2.0.0',
 'pre-commit>=2.7.1,<3.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'cognite-air-sdk',
    'version': '4.0.0',
    'description': 'Client library for AIR, built on top of Cognite Functions in Cognite Data Fusion (CDF)',
    'long_description': 'None',
    'author': 'Håkon V. Treider',
    'author_email': 'hakon.treider@cognite.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
