# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hashpoll_cli', 'hashpoll_cli.helpers']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'rich>=12.5.1,<13.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['hashpoll = hashpoll_cli.__main__:app']}

setup_kwargs = {
    'name': 'hashpoll-cli',
    'version': '0.1.0',
    'description': 'A handy CLI tool for creating polls for Hashnode.\n Made with ❤️ by @hashpoll.',
    'long_description': '',
    'author': 'Arpan Pandey',
    'author_email': 'arpan@hackersreboot.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arpan-206/hahspoll-front',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
