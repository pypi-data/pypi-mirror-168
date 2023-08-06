# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_rss', 'fastapi_rss.models']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.85.0,<1.0.0', 'lxml>=4.7.1,<5.0.0']

setup_kwargs = {
    'name': 'fastapi-rss',
    'version': '0.2.0',
    'description': 'A library to generate RSS feeds for FastAPI',
    'long_description': None,
    'author': 'Dogeek',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
