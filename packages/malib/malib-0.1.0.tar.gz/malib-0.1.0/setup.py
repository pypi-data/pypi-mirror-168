# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'malib',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Louis Abraham',
    'author_email': 'louis.abraham@yahoo.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
