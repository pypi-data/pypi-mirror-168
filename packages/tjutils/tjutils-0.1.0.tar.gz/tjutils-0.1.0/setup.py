# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tjutils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tjutils',
    'version': '0.1.0',
    'description': 'Python Utilities for TJ P',
    'long_description': '# TJUtils (Python)\n',
    'author': 'TJ P',
    'author_email': 'mail@tjpalanca.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
