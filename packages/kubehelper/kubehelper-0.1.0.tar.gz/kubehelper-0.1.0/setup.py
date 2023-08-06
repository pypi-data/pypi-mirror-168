# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kubehelper']

package_data = \
{'': ['*']}

install_requires = \
['pathlib>=1.0.1,<2.0.0', 'ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'kubehelper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'oliver-g-alexander',
    'author_email': 'oliver.g.alexander@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
