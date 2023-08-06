# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dddg', 'dddg.config', 'dddg.inference']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.3,<2.0.0',
 'opencv-python==4.5.5.62',
 'requests>=2.28.1,<3.0.0',
 'torch>=1.12.1,<2.0.0',
 'torchvision>=0.13.1,<0.14.0',
 'webcolors>=1.12,<2.0']

entry_points = \
{'console_scripts': ['dddg = dddg.__main__:main']}

setup_kwargs = {
    'name': 'dddg',
    'version': '0.1.0',
    'description': 'dddg game solver',
    'long_description': '# dddg\nMachine Learning Ducky Labeling and dddg game solver.\n\n![example](https://cdn.ionite.io/img/fIUvgt.jpg)\n\n## Tldr how to use\n```shell\npip install dddg\n```\n> `Usage: dddg [OPTIONS] URL`\n```shell\ndddg https://cdn.ionite.io/img/Rjj91N.jpg\n0 5 11\n1 3 10\n4 7 9\n2 5 9\n3 6 7\n6 9 10\n1 4 6\n```\n\n## Introduction\n\nDuck Duck Duck Goose (dddg) is a game whose objective is to\nfind all "schools" of ducks. A valid school is defined where\neach duck can either have the same or different attributes.\n\n![duck_e1](https://cdn.ionite.io/img/Rjj91N.jpg)\n\n- Each card has 4 features\n  - Color, Number, Hat, and Accessory\n- A valid flight\n  - 3 cards where each feature is either all same or all different\n  - ![duck2](https://cdn.ionite.io/img/Lgy1TX.jpg)\n\n\n## Requirements\n- torch\n- torchvision\n- opencv-python\n- requests\n- webcolors\n\n## Model\n\nDescription WIP\n\n![training](https://cdn.ionite.io/img/l8frRh.jpg)\n',
    'author': 'ionite34',
    'author_email': 'dev@ionite.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
