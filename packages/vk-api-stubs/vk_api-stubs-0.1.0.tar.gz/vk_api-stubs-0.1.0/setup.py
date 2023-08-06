# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vk_api-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vk-api-stubs',
    'version': '0.1.0',
    'description': 'Stubs for vk_api',
    'long_description': None,
    'author': 'sergey',
    'author_email': 'saalaus2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
