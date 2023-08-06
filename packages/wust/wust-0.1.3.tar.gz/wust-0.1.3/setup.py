# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wust']

package_data = \
{'': ['*']}

install_requires = \
['intake>=0.6.5', 'matplotlib>=3.5.2', 'netCDF4>=1.5.7', 'xarray>=0.20.1']

setup_kwargs = {
    'name': 'wust',
    'version': '0.1.3',
    'description': 'WEkEO User Support Toolbox contains a set of tools to ease work in WEkEO.',
    'long_description': '',
    'author': 'David Bazin',
    'author_email': 'dbazin@wekeo.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
