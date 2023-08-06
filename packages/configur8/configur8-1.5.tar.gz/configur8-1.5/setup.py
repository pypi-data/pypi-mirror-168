# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['configur8']

package_data = \
{'': ['*']}

install_requires = \
['email-validator>=1,<2']

setup_kwargs = {
    'name': 'configur8',
    'version': '1.5',
    'description': 'Type-safe configuration and validation library',
    'long_description': 'None',
    'author': 'Nick Joyce',
    'author_email': 'nick@stratuscode.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
