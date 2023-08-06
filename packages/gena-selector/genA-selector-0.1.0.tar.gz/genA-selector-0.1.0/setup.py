# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gena_selector']

package_data = \
{'': ['*']}

install_requires = \
['deap>=1.3.3,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'gena-selector',
    'version': '0.1.0',
    'description': 'Feature selection with genetic algorithm.',
    'long_description': None,
    'author': 'Pavel Kochkin',
    'author_email': 'kochkin27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
