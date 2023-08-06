# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb', 'lb.nightly.db']

package_data = \
{'': ['*']}

install_requires = \
['cloudant>=2.14.0,<3.0.0', 'lb-nightly-configuration>=0.3,<0.4']

setup_kwargs = {
    'name': 'lb-nightly-db',
    'version': '0.2.0',
    'description': 'Database access layer for LHCb Nightly and Continuous Integration Build System',
    'long_description': 'None',
    'author': 'Marco Clemencic',
    'author_email': 'marco.clemencic@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
