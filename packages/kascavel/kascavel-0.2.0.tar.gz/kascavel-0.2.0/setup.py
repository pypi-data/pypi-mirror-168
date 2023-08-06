# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kascavel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kascavel',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'cassio.souza',
    'author_email': 'cassio.souza@grupotel.com.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
