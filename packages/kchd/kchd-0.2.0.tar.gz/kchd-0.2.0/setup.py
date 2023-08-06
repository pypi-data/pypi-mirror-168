# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kchd', 'kchd.controllers']

package_data = \
{'': ['*']}

install_requires = \
['astoria>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['kchd = kchd:main']}

setup_kwargs = {
    'name': 'kchd',
    'version': '0.2.0',
    'description': 'KCH LED Daemon',
    'long_description': None,
    'author': 'Dan Trickey',
    'author_email': 'dtrickey@studentrobotics.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
