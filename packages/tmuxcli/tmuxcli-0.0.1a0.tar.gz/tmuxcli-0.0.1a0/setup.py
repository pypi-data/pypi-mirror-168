# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tmuxcli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tmuxcli',
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
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
