# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyathena_lite']

package_data = \
{'': ['*']}

install_requires = \
['pyathena>=2.14.0,<3.0.0', 'pytest>=7.1.3,<8.0.0']

setup_kwargs = {
    'name': 'pyathena-lite',
    'version': '0.1.0',
    'description': 'Simple pyathena connector',
    'long_description': '',
    'author': 'Prabhu ',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
