# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ogero', 'ogero.asyncio']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pyogero',
    'version': '0.1.0',
    'description': 'Ogero API module',
    'long_description': '# pyOgero: Ogero API Python module\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pyogero)](https://pypi.org/project/pyogero/)\n[![Package Status](https://img.shields.io/pypi/status/pyogero)](https://pypi.org/project/pyogero/)\n[![GitHub branch checks state](https://img.shields.io/github/checks-status/oraad/pyogero/main)](https://github.com/oraad/pyogero/)\n[![License](https://img.shields.io/pypi/l/pyogero)](https://github.com/oraad/pyogero/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)\n\nOgero does not currently provide a rest api to access it services,\ntherefore this module web scrap the mobile version of the pages to collect data.\n',
    'author': 'Omar Raad',
    'author_email': 'omarraad@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/oraad/pyogero',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
