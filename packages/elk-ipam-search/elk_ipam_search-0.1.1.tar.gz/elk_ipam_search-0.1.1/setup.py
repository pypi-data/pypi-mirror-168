# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elk_ipam_search', 'elk_ipam_search.utils']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.16.1,<7.17.0', 'mailru-im-bot==0.0.21']

setup_kwargs = {
    'name': 'elk-ipam-search',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'Ilya Zakharov',
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
