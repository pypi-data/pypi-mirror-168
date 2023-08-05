# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uql', 'uql.utils']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.1,<5.0', 'django-rest-framework>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'uql',
    'version': '0.1.0',
    'description': 'Application layer for building Django apps with a breeze',
    'long_description': 'None',
    'author': 'rubbie kelvin voltsman',
    'author_email': 'rubbiekelvinvoltsman@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
