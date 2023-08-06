# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nexcsi']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.3,<2.0.0']

setup_kwargs = {
    'name': 'nexcsi',
    'version': '0.1.0',
    'description': 'A fast and simple decoder for Nexmon_CSI',
    'long_description': 'None',
    'author': 'Aravind Reddy Voggu',
    'author_email': 'zerodividedby0@gmail.com',
    'maintainer': 'Aravind Reddy Voggu',
    'maintainer_email': 'zerodividedby0@gmail.com',
    'url': 'https://github.com/nexmonster/nexcsi.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
