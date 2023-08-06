# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pepver']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pepver',
    'version': '1.0.0rc1',
    'description': 'PEP-440 version parsing, interpretation and manipulation',
    'long_description': '======\npepver\n======\n\nPEP-440 version parsing, interpretation and manipulation\n',
    'author': 'technomunk',
    'author_email': 'thegriffones@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/technomunk/pepver',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
