# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kamino', 'kamino.cli', 'kamino.core', 'kamino.core.respository']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.9.1,<5.0.0']

setup_kwargs = {
    'name': 'kamino',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Samuel Nogueira Bacelar',
    'author_email': 'samuelnbacelar@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
