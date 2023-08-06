# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vk_api-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vk-api-stubs',
    'version': '1.0.0',
    'description': 'Stubs for vk_api module',
    'long_description': '## vk_api-stubs\n\nСтабы для модуля vk_api\n\n100% покрытие типов + типы для методов API\n\n## Зачем?\nСтабы нужны для проверки типов и автодополнения в IDE\n\n## Установка\n`pip install vk_api-stubs`',
    'author': 'sergey',
    'author_email': 'saalaus2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saalaus/vk_api-stubs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
