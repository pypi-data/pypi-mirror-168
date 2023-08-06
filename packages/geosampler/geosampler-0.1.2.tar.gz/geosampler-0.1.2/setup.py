# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geosampler']

package_data = \
{'': ['*']}

install_requires = \
['folium>=0.12.1,<0.13.0',
 'pandas>=1.5.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'geosampler',
    'version': '0.1.2',
    'description': 'A simple way to collect samples for social sciences experiments',
    'long_description': None,
    'author': 'Gloria Macia',
    'author_email': 'gloria.macia@roche.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
