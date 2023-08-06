# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['diffren_jax']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'diffren-jax',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'fcole',
    'author_email': 'fcole@google.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
