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
    'version': '0.4.1',
    'description': 'Manage gmail account using python, forget about imap and just code what you supposed to do.',
    'long_description': '# GGmail\n\n[![GGmail Continuous Integration](https://github.com/dylandoamaral/ggmail/actions/workflows/ci.yml/badge.svg)](https://github.com/dylandoamaral/ggmail/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/dylandoamaral/ggmail/branch/main/graph/badge.svg?token=KY5JTQWZLF)](https://codecov.io/gh/dylandoamaral/ggmail)\n[![PyPI version](https://badge.fury.io/py/ggmail.svg)](https://badge.fury.io/py/ggmail)\n[![downloads](https://pepy.tech/badge/ggmail/month)](https://pepy.tech/project/ggmail)\n[![versions](https://img.shields.io/pypi/pyversions/ggmail.svg)](https://github.com/dylandoamaral/ggmail)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nManage mail account using python, forget about imap and just code what you supposed to do.\n\n## Help\n\nSee [documentation](https://github.com/dylandoamaral/ggmail/wiki) for more details.\n\n## Install\n\nInstall using `pip install ggmail`.\n\n## A Simple Example\n\n```python\nfrom ggmail import Account, Google\nfrom ggmail.policy import from_contains, flagged\n\nauthentication = Google(username="ggmail@gmail.com", password="secret")\nwith Account(authentication=authentication) as account:\n    inbox = account.inbox()\n    mailbox = account.create_mailbox("Favorite")\n    policy = from_contains("from@gmail.com") + flagged\n    messages = inbox.search(policy)\n\n    for message in messages:\n        message.copy(mailbox)\n```\n\n## Additional Information\n\n### Why not use imbox instead ?\n\nhttps://github.com/martinrusev/imbox is less high level than ggmail. I wanted something even more human than imbox.\n\n### Why not use gmail instead ?\n\nhttps://github.com/charlierguo/gmail seems to be dead.\n\n## You don\'t support my mail provider ?\n\nYou can raise an issue and I will add it.\n',
    'author': 'dylandoamaral',
    'author_email': 'do.amaral.dylan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dylandoamaral/ggmail',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
