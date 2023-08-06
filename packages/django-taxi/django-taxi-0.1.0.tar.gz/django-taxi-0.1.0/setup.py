# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_taxi', 'django_taxi.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0,<5.0', 'pre-commit>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'django-taxi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Nibon',
    'author_email': 'daniel@nibon.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
