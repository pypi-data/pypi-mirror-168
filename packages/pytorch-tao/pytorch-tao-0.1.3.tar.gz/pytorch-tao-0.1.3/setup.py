# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_tao']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['tao = pytorch_tao.cli:main']}

setup_kwargs = {
    'name': 'pytorch-tao',
    'version': '0.1.3',
    'description': 'Tao for PyTorch',
    'long_description': 'None',
    'author': 'chenglu',
    'author_email': 'chenglu.she@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
