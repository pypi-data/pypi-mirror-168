# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htmx_gen']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'htmx-gen',
    'version': '1.0.0',
    'description': 'Generate HTML conveniently and efficiently',
    'long_description': None,
    'author': 'Pierre',
    'author_email': 'pierre.carbonnelle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
