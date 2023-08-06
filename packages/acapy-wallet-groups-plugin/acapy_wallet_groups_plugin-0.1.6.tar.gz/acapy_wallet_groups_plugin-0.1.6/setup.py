# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acapy_wallet_groups_plugin']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'aries-cloudagent[indy]==0.7.4',
 'marshmallow>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'acapy-wallet-groups-plugin',
    'version': '0.1.6',
    'description': 'Agent plugin to add a group id to a wallet',
    'long_description': 'None',
    'author': 'Berend Sliedrecht',
    'author_email': 'berend@animo.id',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<3.10.0',
}


setup(**setup_kwargs)
