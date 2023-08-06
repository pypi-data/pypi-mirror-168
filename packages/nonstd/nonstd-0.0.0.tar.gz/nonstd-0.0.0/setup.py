# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonstd']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.3,<8.0.0', 'scipy>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'nonstd',
    'version': '0.0.0',
    'description': "Tom's non-standard library of useful classes and functions.",
    'long_description': "Tom's non-standard library of useful classes and functions.",
    'author': 'tadamcz',
    'author_email': 'tadamczewskipublic@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
