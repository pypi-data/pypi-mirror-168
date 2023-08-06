# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bina']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.3,<2.0.0',
 'opencv-python>=4.6.0.66,<5.0.0.0',
 'pendulum>=2.1,<3.0']

setup_kwargs = {
    'name': 'bina',
    'version': '0.1.1',
    'description': 'Python Multi-Camera Recording and Synchronization',
    'long_description': '',
    'author': 'Ahmad Amirivojdan',
    'author_email': 'aamirivo@vols.utk.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
