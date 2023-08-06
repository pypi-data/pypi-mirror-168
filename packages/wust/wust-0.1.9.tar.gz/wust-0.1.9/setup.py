# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wust']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=3.6,<4.0',
 'intake-thredds>=2021.6.16',
 'matplotlib>=3.5.2',
 'netcdf4>=1.6.0']

setup_kwargs = {
    'name': 'wust',
    'version': '0.1.9',
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
