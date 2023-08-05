# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sheval']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sheval',
    'version': '1.0.4',
    'description': 'Safely evaluate mathematical and logical expressions.',
    'long_description': "# 🐴 sheval\n\nSafely evaluate mathematical and logical expressions. Most operations are supported.\n\n### Whitelisted data types\nFor security, only certain data types are allowed:<br>\n`str`, `int`, `float`, `complex`, `list`, `tuple`, `set`, `dict`, `bool`, `bytes`, `NoneType`\n\n## Example\n\n```py\nfrom sheval import sheval\n\n_locals = dict(x=3, y=1, z=4)\n\nsheval('x > y <= z', _locals)\n```",
    'author': 'Maximillian Strand',
    'author_email': 'maxi@millian.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/deepadmax/deval',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
