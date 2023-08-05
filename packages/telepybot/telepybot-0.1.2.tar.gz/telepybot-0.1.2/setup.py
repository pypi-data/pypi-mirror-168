# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telepybot', 'telepybot.helpers', 'telepybot.models', 'telepybot.types']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.4,<38.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'telepybot',
    'version': '0.1.2',
    'description': "A Python class to help you interact with Telegram's bot api.",
    'long_description': "# Telepybot\nPython client for making your own Telegram bot!\n\nIt has support for webhooks and it automatically handles the setup of self-signed SSL certificates, so you can run it even on a Raspberry Pi or any other home server/laptop (find an example of this in [`examples/webhook_setup.py`](https://github.com/omirete/telepybot/blob/master/examples/webhook_setup.py)).\n\nInstall with:\n```\npip -m install telepybot\n```\n\nTo use it, just import the Telepybot class and pass it your bot's token:\n```python\n# Sending a simple message\nfrom telepybot import Telepybot\n\ntelepybot = Telepybot(token='YOUR_BOT_API_TOKEN')\n\nuser_id = '123456'\ntelepybot.sendMsg(user_id, 'This message was sent using Telepybot!')\n```\n\nSee the [`examples/`](https://github.com/omirete/telepybot/tree/master/examples) directory for more examples.\n\nFeel free to use it for your own projects and be sure to create issues if something is not working right. Pull requests and feature requests are welcome.\n\n## How to get an API Token?\nYou can generate one using the [official instructions](https://core.telegram.org/bots/api#authorizing-your-bot) from Telegram, it should be fairly straightforward.\n",
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
