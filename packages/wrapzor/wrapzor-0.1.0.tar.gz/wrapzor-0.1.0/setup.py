# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.api',
 'src.api.metadata',
 'src.core',
 'src.models',
 'src.models.metadata']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'piou>=0.11.0,<0.12.0', 'pydantic>=1.9.2,<2.0.0']

entry_points = \
{'console_scripts': ['cli = run:run']}

setup_kwargs = {
    'name': 'wrapzor',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'abonur',
    'author_email': 'sm7.abonur@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
