# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_vcs']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['sphinx = pytest_vcs']}

setup_kwargs = {
    'name': 'pytest-vcs',
    'version': '0.0.1a0',
    'description': '',
    'long_description': '',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
