# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rira']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rira',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Ahmad Amirivojdan',
    'author_email': 'aamirivo@vols.utk.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
