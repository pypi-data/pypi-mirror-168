# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synnax', 'synnax.channel', 'synnax.segment']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.971,<0.972',
 'pandas>=1.4.3,<2.0.0',
 'synnax-freighter>=0.1.1,<0.2.0',
 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'synnax',
    'version': '0.1.2',
    'description': 'Synnax Client Library',
    'long_description': None,
    'author': 'emiliano bonilla',
    'author_email': 'emilbon99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://synnaxlabs.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
