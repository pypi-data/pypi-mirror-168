# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['empower']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.3,<8.0.0', 'wrapt>=1.11,<2.0']

setup_kwargs = {
    'name': 'empower',
    'version': '0.2.1',
    'description': 'Goodbye Inheritance',
    'long_description': '# empower\n\nGoodbye Inheritance!!!\n\n## Install\n\n```python\npip install empower\n```\n\n## Usage\n\nYou have a `Duck` class without any methods.\n\n```python\n# mod/__init__.py\n\nclass Duck:\n    ...\n```\n\nYou define a trait `Fly` for `Duck`\n```python\n# mod/fly.py\n\nfrom empower import impl, Trait\n\nfrom . import Duck\n\n@impl(Duck)\nclass Fly(Trait):\n    def fly(self):\n        return "fly"\n```\n\nAnd you define another trait `Run` for `Duck`\n```python\n# mod/run.py\n\nfrom empower import impl, Trait\n\nfrom . import Duck\n\n\n@impl(Duck)\nclass Run(Trait):\n    def run(self):\n        return "run"\n```\n\nNow you can add empower `Duck`\n```python\n# main.py\n\nfrom mod import Duck\nfrom empower import use\n\nduck = Duck()\n\nuse("mod.fly")  # load fly trait\nuse("mod.run")  # load run trait\n\nassert duck.fly() == "fly"\nassert duck.run() == "run"\n```',
    'author': 'ZhengYu, Xu',
    'author_email': 'zen-xu@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
