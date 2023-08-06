# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb', 'lb.nightly.rpc']

package_data = \
{'': ['*']}

install_requires = \
['celery[sqlalchemy]>=5.1.2,<6.0.0',
 'lb-nightly-configuration>=0.3,<0.4',
 'lbplatformutils>=4.3.6,<5.0.0',
 'mysqlclient>=2.0.3,<3.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'lb-nightly-rpc',
    'version': '0.2.0',
    'description': 'Celery inter-process interface for LHCb Nightly and Continuous Integration Build System',
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
