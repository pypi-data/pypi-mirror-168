# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma', 'sigma.backends.qradar', 'sigma.pipelines.qradar']

package_data = \
{'': ['*']}

install_requires = \
['pysigma>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'pysigma-backend-qradar',
    'version': '0.2.1',
    'description': 'pySigma Qradar backend',
    'long_description': 'None',
    'author': 'nNipsx-Sec',
    'author_email': 'nnipsxz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
