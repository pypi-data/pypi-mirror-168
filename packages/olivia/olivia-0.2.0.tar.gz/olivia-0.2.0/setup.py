# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olivia']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'olivia',
    'version': '0.2.0',
    'description': 'Assistente para facilitar requisições HTTP',
    'long_description': '',
    'author': 'matheus',
    'author_email': 'matheus.mmn@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
