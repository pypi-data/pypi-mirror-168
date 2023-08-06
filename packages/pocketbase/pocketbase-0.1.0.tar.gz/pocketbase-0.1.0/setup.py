# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pocketbase',
 'pocketbase.models',
 'pocketbase.models.utils',
 'pocketbase.services',
 'pocketbase.services.utils',
 'pocketbase.stores']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'pocketbase',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Vithor Jaeger',
    'author_email': 'vaphes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
