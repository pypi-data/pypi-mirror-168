# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['surrealdb', 'surrealdb.clients', 'surrealdb.common', 'surrealdb.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1', 'httpx>=0.23.0']

setup_kwargs = {
    'name': 'surrealdb',
    'version': '0.1.0',
    'description': 'The official SurrealDB library for Python.',
    'long_description': 'None',
    'author': 'SurrealDB',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
