# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odeanimate', 'odeanimate.methods', 'odeanimate.plots']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0', 'matplotlib>=3.5.2,<4.0.0']

setup_kwargs = {
    'name': 'odeanimate',
    'version': '0.0.3',
    'description': 'A module for useful quick mathematical calculation, plotting and animation.',
    'long_description': 'None',
    'author': 'Miguel Alejandro Salgado Zapien',
    'author_email': 'ekiim@ekiim.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
