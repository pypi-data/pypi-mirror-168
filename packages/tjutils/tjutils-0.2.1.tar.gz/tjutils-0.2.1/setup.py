# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tjutils']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'bandit>=1.7.4,<2.0.0',
 'black>=22.8.0,<23.0.0',
 'fastcore>=1.5.27,<2.0.0',
 'flake8>=5.0.4,<6.0.0',
 'ipykernel>=6.15.3,<7.0.0',
 'mypy>=0.971,<0.972',
 'nbdev>=2.3.6,<3.0.0']

entry_points = \
{'console_scripts': ['tjdev_export = tjutils.nbdev:export',
                     'tjdev_generate = tjutils.nbdev:generate',
                     'tjdev_version = tjutils.nbdev:version']}

setup_kwargs = {
    'name': 'tjutils',
    'version': '0.2.1',
    'description': 'Python Utilities for TJ P',
    'long_description': '# TJUtils (Python)\n\nThis is a set of utilities to assist in development in Python. See the notebooks folder for the various functionality included in this package.\n',
    'author': 'TJ P',
    'author_email': 'mail@tjpalanca.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
