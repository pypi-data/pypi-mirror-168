# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['empower']

package_data = \
{'': ['*']}

install_requires = \
['wrapt>=1.11,<2.0']

setup_kwargs = {
    'name': 'empower',
    'version': '0.2.0',
    'description': 'Goodbye Inheritance',
    'long_description': None,
    'author': 'ZhengYu, Xu',
    'author_email': 'zen-xu@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
