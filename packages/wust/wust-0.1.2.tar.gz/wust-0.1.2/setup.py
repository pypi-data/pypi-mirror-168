# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wust']

package_data = \
{'': ['*']}

install_requires = \
['Bottleneck>=1.3.5,<2.0.0',
 'dask>=2022.9.1,<2023.0.0',
 'intake>=0.6.6,<0.7.0',
 'ipykernel>=6.15.3,<7.0.0',
 'matplotlib>=3.6.0,<4.0.0',
 'netCDF4>=1.6.1,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'xarray>=2022.6.0,<2023.0.0']

setup_kwargs = {
    'name': 'wust',
    'version': '0.1.2',
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
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
