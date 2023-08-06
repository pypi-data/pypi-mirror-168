# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_cli_run']

package_data = \
{'': ['*']}

install_requires = \
['pardoc>=0.0,<0.1', 'pipen-args>=0.3,<0.4', 'pipen>=0.3,<0.4']

entry_points = \
{'pipen_cli': ['cli-run = pipen_cli_run:PipenCliRunPlugin']}

setup_kwargs = {
    'name': 'pipen-cli-run',
    'version': '0.2.1',
    'description': 'A pipen cli plugin to run a process or a pipeline',
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
