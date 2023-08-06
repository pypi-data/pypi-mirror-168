# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'malib',
    'version': '0.1.1',
    'description': '',
    'long_description': '# malib\n\nA few utilities that I find useful.\n\n\n## RateLimiter\n\n```py\n# call a function at most 10 times per minute\nrl = RateLimiter(max_calls=10, period=60) \n# call .wait() every time before calling the function\nrl.wait()\n```\n\n\n## Testing\n\n`pytest`\n\n',
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
