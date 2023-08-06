# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ggmail']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'ggmail',
    'version': '0.4.0',
    'description': 'Manage gmail account using python, forget about imap and just code what you supposed to do.',
    'long_description': 'None',
    'author': 'dylandoamaral',
    'author_email': 'do.amaral.dylan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
