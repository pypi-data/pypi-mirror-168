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
    'version': '0.1.3',
    'description': 'PocketBase SDK for python.',
    'long_description': '# PocketBase Python SDK\n\n[![Python 3.7-3.10](https://github.com/vaphes/pocketbase/actions/workflows/python-versions.yml/badge.svg)](https://github.com/vaphes/pocketbase/actions/workflows/python-versions.yml)\n\nPython client SDK for the <a href="https://pocketbase.io/">PocketBase</a> backend.\n\nThis is in early development, and at first is just a translation of <a href="https://github.com/pocketbase/js-sdk">the javascript lib</a> using <a href="https://github.com/encode/httpx/">HTTPX</a>.\n\n---\n\nInstall PocketBase using pip:\n\n```shell\n$ pip install pocketbase\n```\n\n<p align="center"><i>The PocketBase Python SDK is <a href="https://github.com/vaphes/pocketbase/blob/master/LICENCE.txt">MIT licensed</a> code.</p>',
    'author': 'Vithor Jaeger',
    'author_email': 'vaphes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vaphes/pocketbase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
