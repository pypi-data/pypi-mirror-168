# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_cli_init']

package_data = \
{'': ['*'], 'pipen_cli_init': ['templates/*']}

install_requires = \
['cmdy>=0.5,<0.6', 'pipen>=0.3,<0.4', 'poetry>=1,<2']

entry_points = \
{'pipen_cli': ['cli-init = pipen_cli_init:PipenCliInit']}

setup_kwargs = {
    'name': 'pipen-cli-init',
    'version': '0.1.1',
    'description': 'A pipen cli plugin to create a pipen project (pipeline)',
    'long_description': 'None',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
