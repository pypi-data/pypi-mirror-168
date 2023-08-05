# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ansie']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ansie',
    'version': '0.0.2',
    'description': 'Utility for convenient use of ANSI ESC codes.',
    'long_description': None,
    'author': 'Rebzzel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
