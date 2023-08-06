# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['replit_bot', 'replit_bot.utils']

package_data = \
{'': ['*'], 'replit_bot': ['templates/*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'datauri>=1.0.0,<2.0.0',
 'replit>=3.2.4,<4.0.0',
 'requests>=2.28.1,<3.0.0',
 'waitress>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'replit-bot',
    'version': '1.1.4',
    'description': '',
    'long_description': None,
    'author': 'bigminboss',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9',
}


setup(**setup_kwargs)
