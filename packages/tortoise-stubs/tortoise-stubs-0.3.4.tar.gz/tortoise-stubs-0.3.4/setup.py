# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tortoise-stubs']

package_data = \
{'': ['*'], 'tortoise-stubs': ['fields/*']}

install_requires = \
['tortoise-orm']

setup_kwargs = {
    'name': 'tortoise-stubs',
    'version': '0.3.4',
    'description': '',
    'long_description': None,
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
