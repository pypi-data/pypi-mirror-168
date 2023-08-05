# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telepybot', 'telepybot.models', 'telepybot.types']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.4,<38.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'telepybot',
    'version': '0.1.0',
    'description': "A Python class to help you interact with Telegram's bot api.",
    'long_description': '',
    'author': 'Federico Giancarelli',
    'author_email': 'hello@federicogiancarelli.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
