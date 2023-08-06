# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pepver']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pepver',
    'version': '1.0.0rc0',
    'description': 'PEP-440 version parsing, interpretation and manipulation',
    'long_description': None,
    'author': 'technomunk',
    'author_email': 'thegriffones@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
