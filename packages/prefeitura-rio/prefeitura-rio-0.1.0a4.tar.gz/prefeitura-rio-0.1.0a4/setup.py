# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prefeitura_rio', 'prefeitura_rio.metrics']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.3,<2.0.0', 'scikit-learn>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['docs = scripts.docs:main',
                     'lint = scripts.lint:main',
                     'test = scripts.test:main']}

setup_kwargs = {
    'name': 'prefeitura-rio',
    'version': '0.1.0a4',
    'description': 'Pacote Python que implementa utilidades para nossos projetos!',
    'long_description': '# prefeitura-rio\n\nUm pacote Python que implementa utilidades para nossos projetos!\n',
    'author': 'Gabriel Gazola Milan',
    'author_email': 'gabriel.gazola@poli.ufrj.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/prefeitura-rio/prefeitura-rio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
