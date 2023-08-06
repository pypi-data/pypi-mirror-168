# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_tao']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytorch-tao',
    'version': '0.1.0',
    'description': 'Tao for PyTorch',
    'long_description': None,
    'author': 'chenglu',
    'author_email': 'chenglu.she@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
