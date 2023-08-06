# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nixos_compose',
 'nixos_compose.commands',
 'nixos_compose.driver',
 'nixos_compose.flavours',
 'nixos_compose.tools']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=7.1.2',
 'execo>=2.6.8,<3.0.0',
 'halo>=0.0.31,<0.0.32',
 'pexpect>=4.8.0,<5.0.0',
 'psutil>=5.9.0,<6.0.0',
 'ptpython>=3.0.7,<4.0.0',
 'pyinotify>=0.9.6,<0.10.0',
 'requests>=2.27.1,<3.0.0',
 'tomlkit>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['nixos-compose = nixos_compose.cli:main',
                     'nxc = nixos_compose.cli:main']}

setup_kwargs = {
    'name': 'nixos-compose',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Olivier Richard',
    'author_email': 'olivier.richard@imag.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
