# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pepver']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pepver',
    'version': '1.0.0rc3',
    'description': 'PEP-440 version parsing, interpretation and manipulation',
    'long_description': '# pepver\n\n[![Python versions](https://img.shields.io/pypi/pyversions/pepver.svg)](https://pypi.org/project/pepver)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Unit tests](https://github.com/technomunk/pepver/actions/workflows/test.yml/badge.svg)](https://github.com/technomunk/pepver/actions/workflows/test.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPEP-440 version parsing, interpretation and manipulation.\n\n```py\n>>> from pepver import Version\n>>> version = Version.parse("0!1.2.3.4a5.post6.dev7+8.9")\n>>> version.epoch\n0\n>>> version.release\n(1, 2, 3, 4)\n>>> version.major\n1\n>>> version.minor\n2\n>>> version.micro\n3\n>>> version.pre\n(\'a\', 5)\n>>> version.post\n6\n>>> version.dev\n7\n>>> version.local\n\'8.9\'\n```\n\n## Usage\n\nThe main star of the library is the `Version` class, which encompasses the semantics of a version string.\nIt can be instantiated directly or be parsed from a string:\n```py\n>>> from pepver import Version\n>>> Version(1, 2, 3, 4)\nValue(release=(1,), pre=2, post=3, dev=4)\n>>> Version((0, 1, 2, 3), post=11, epoch=1)\nValue(epoch=1, release=(0, 1, 2, 3), post=11)\n>>> Version.parse("11.2")\nValue(release=(11, 2))\n```\n\nVersions can be updated to suit one\'s needs:\n```py\n>>> from pepver import Version\n>>> version = Version.parse("0!1.2.3.4a5.post6.dev7+8.9")\n>>> version.update("minor")\nValue(epoch=0, release=(1, 3))\n>>> version.update("post", -2)\nValue(epoch=0, release=(1, 2, 3, 4), pre=(\'a\', 5), post=4)\n>>> version.update("release")\nValue(epoch=0, release=(1, 2, 3, 5))\n>>> version.update("release").is_final()\nTrue\n```\n\nVersions correctly convert into strings. Note that the conversion is "normalized" ie\nstandard representation that is the same for the same version:\n\n```py\n>>> from pepver import Version\n>>> str(Version.parse("010.12-11"))\n\'10.12.post11\'\n>>> str(Version.parse("1.2.3preview11dev"))\n\'1.2.3rc11.dev0\'\n```\n',
    'author': 'technomunk',
    'author_email': 'thegriffones@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/technomunk/pepver',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
