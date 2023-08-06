# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlner']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['hlner = hlner.main:lner', 'unhlner = hlner.main:unlner']}

setup_kwargs = {
    'name': 'hlner',
    'version': '0.1.0',
    'description': 'Create and remove hard directory links',
    'long_description': '',
    'author': 'mush42',
    'author_email': 'musharraf.omer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
