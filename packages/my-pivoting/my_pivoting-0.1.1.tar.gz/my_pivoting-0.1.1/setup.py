# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_pivoting']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'my-pivoting',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Egor Krapivin',
    'author_email': 'egor.krapivin98@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
