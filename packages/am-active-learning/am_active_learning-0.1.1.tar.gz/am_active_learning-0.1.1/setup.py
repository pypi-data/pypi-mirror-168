# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['am_active_learning',
 'am_active_learning.src',
 'am_active_learning.src.data_tools']

package_data = \
{'': ['*']}

install_requires = \
['botorch>=0.6.5,<0.7.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.22.4,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'sklearn>=0.0,<0.1',
 'torch>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'am-active-learning',
    'version': '0.1.1',
    'description': 'Active Learning package for composition and process optimization.',
    'long_description': None,
    'author': 'Ayush Jain',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
