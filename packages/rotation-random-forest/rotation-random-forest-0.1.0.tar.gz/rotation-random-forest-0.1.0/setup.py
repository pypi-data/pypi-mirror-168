# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rotation_random_forest']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.3,<2.0.0', 'scikit-learn>=1.1.2,<2.0.0', 'scipy>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'rotation-random-forest',
    'version': '0.1.0',
    'description': 'Implementation Rotation Random Forest with interface like scikit-learn.',
    'long_description': None,
    'author': 'Pavel Kochkin',
    'author_email': 'kochkin27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
