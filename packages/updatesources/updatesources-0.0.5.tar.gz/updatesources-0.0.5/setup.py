# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cmaketools', 'cmaketools.internal', 'cmaketools.internal.updatesources']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['updatesources = cmaketools.updatesources:main']}

setup_kwargs = {
    'name': 'updatesources',
    'version': '0.0.5',
    'description': 'Generate a cmake file which sets a list of files to a cmake variable',
    'long_description': None,
    'author': 'Nicholas Johnson',
    'author_email': 'nicholas.m.j@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
