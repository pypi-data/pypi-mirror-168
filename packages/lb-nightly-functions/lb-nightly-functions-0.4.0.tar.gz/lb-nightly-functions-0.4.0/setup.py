# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb', 'lb.nightly.functions']

package_data = \
{'': ['*'],
 'lb.nightly.functions': ['data/*', 'data/cmake/*', 'data/cmake/modules/*']}

install_requires = \
['GitPython>=3.1.18,<4.0.0',
 'archspec>=0.1.2,<0.2.0',
 'lb-nightly-configuration>=0.3,<0.4',
 'lb-nightly-db>=0.2,<0.3',
 'lb-nightly-utils>=0.4,<0.5',
 'lbplatformutils>=4.3.8,<5.0.0',
 'python-gitlab>=3.9.0,<4.0.0']

entry_points = \
{'console_scripts': ['lb-wrapcmd = lb.nightly.functions.common:lb_wrapcmd'],
 'lb.nightly.checkout_methods': ['git = lb.nightly.functions.checkout:git']}

setup_kwargs = {
    'name': 'lb-nightly-functions',
    'version': '0.4.0',
    'description': 'Core functions for LHCb Nightly and Continuous Integration Build System',
    'long_description': 'None',
    'author': 'Marco Clemencic',
    'author_email': 'marco.clemencic@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
