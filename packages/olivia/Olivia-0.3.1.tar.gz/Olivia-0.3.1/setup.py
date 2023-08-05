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
    'version': '0.3.1',
    'description': 'Assistente para facilitar requisições HTTP',
    'long_description': '# Olivia\n\n**Uma simples, amigável e poderosa assistente para requisições HTTP**\n\n- Olivia utiliza a biblioteca *requests*, tornando sua execução mais intuitiva.\n\n## Instalação\n    pip install olivia\n\n## Métodos\nNa versão *0.3.0*, Olivia assite aos métodos *POST, GET, DELETE*\n\n# Modo de Usar\n## POST\n\n``` python\n\nfrom olivia import Olivia\n\ninfos = {\n    "rua": "Verde",\n    "numero": "29"\n}\n\ndados = Olivia("http://url@url.com", infos)\ndados.olivia_salva()\n\n```\n# Olivia\n',
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
