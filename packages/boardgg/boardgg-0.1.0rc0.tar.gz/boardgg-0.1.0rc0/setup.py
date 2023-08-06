# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boardgg', 'boardgg.tests', 'boardgg.tests.mocks', 'boardgg.v1']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.0,<3.0.0', 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'boardgg',
    'version': '0.1.0rc0',
    'description': '',
    'long_description': None,
    'author': 'Pablo Moreno',
    'author_email': 'pablomoreno.inf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
