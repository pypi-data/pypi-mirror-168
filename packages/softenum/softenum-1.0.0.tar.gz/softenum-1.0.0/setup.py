# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['softenum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'softenum',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Javier Junquera-Sánchez',
    'author_email': 'javier@junquera.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
