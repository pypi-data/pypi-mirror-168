# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pepver']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pepver',
    'version': '1.0.0rc2',
    'description': 'PEP-440 version parsing, interpretation and manipulation',
    'long_description': '# pepver\n\n\nPEP-440 version parsing, interpretation and manipulation.\n\n\n```py\nfrom pepver import Version\n\n\nversion = Version.parse("0!1.2.3.4a5.post6.dev7+8.9")\nversion.epoch  # 0\nversion.release  # 1, 2, 3, 4\nversion.major  # 1\nversion.minor  # 2\nversion.micro  # 3\nversion.pre  # a 5\nversion.post  # 6\nversion.dev  # 7\nversion.local  # "8.9"\n\n\nnormalized = Version.parse("00!1.a-5-11dev.1")\nstr(normalized)  # 0!1a5.post11.dev1\n```\n',
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
