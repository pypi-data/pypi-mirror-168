# Telepybot
Python client for making your own Telegram bot!

It has support for webhooks and it automatically handles the setup of self-signed SSL certificates, so you can run it even on a Raspberry Pi or any other home server/laptop (find an example of this in [`examples/webhook_setup.py`](https://github.com/omirete/telepybot/blob/master/examples/webhook_setup.py)).

Install with:
```
pip -m install telepybot
```

To use it, just import the Telepybot class and pass it your bot's token:
```python
# Sending a simple message
from telepybot import Telepybot

telepybot = Telepybot(token='YOUR_BOT_API_TOKEN')

user_id = '123456'
telepybot.sendMsg(user_id, 'This message was sent using Telepybot!')
```

See the [`examples/`](https://github.com/omirete/telepybot/tree/master/examples) directory for more examples.

Feel free to use it for your own projects and be sure to create issues if something is not working right. Pull requests and feature requests are welcome.

## How to get an API Token?
You can generate one using the [official instructions](https://core.telegram.org/bots/api#authorizing-your-bot) from Telegram, it should be fairly straightforward.
