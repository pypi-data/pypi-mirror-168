import requests, json
from typing import Union
from secrets import token_urlsafe

from .helpers import get_public_external_ip, BASE64_ALPHABET_URLSAFE
from telepybot.models import WebhookInfo
from .ssl import Ssl, ServerLocationInfo

class Webhook():
    def __init__(self, base_url: str, debug_mode: bool = False) -> None:
        self.base_url = base_url
    
    @property
    def ssl(self):
        return Ssl()

    def set(self, public_ip: str, webhook_location: str, secret_token: str, public_certificate: bytes = None) -> bool:
        # Content-Type multipart/form-data
        url = f'{self.base_url}/setWebhook'
        payload = {
            "url": f"https://{public_ip}/{webhook_location}?secret_token={secret_token}",
        }
        form_data = {}
        if public_certificate != None:
            form_data["certificate"] = public_certificate
        
        r = requests.post(url, params=payload, files=form_data)
        print(r.text)
        if r.status_code == 200:
            return True
        else:
            r.raise_for_status()
    
    def delete(self, drop_pending_updates: bool = None) -> bool:
        # Content-Type multipart/form-data
        url = f'{self.base_url}/deleteWebhook'
        payload = {}
        if drop_pending_updates != None:
            payload["drop_pending_updates"] = payload
        if payload != {}:
            r = requests.post(url, params=payload)
        else:
            r = requests.post(url)
        print(r.text)
        if r.status_code == 200:
            return True
        else:
            r.raise_for_status()
    
    def getInfo(self) -> WebhookInfo:
        # Content-Type multipart/form-data
        url = f'{self.base_url}/getWebhookInfo'
        r = requests.post(url)
        if r.status_code == 200:
            response_json = r.json()
            if response_json["ok"] == True:
                wh_info = response_json["result"]
                wh_info = WebhookInfo(**wh_info)
                return wh_info
            else:
                raise Exception(f'Response received is not ok. See raw response: {r.text}')
        else:
            r.raise_for_status()

    def autosetup(self, webhook_location: str, use_self_signed_certificate: bool = True, with_secret_token: Union[bool, str] = True):
        """
        [Important note] This method will override any preexisting webhook
        configuration (including self-signed ssl certificate) from your
        Telegram bot.
        
        Arguments:
         - webhook_location: specify the endpoint which Telegram should point the updates to. For example, if you set it to /my-telebot, every time your bot receives a message, Telegram will send a POST request with the information to https://XX.XX.XX.XX/my-telebot, where XX.XX.XX.XX is the public ip (external) of your server.
         - use_self_signed_certificate: If you are not sure what you are doing (or if you are just playing around with this library in your local computer), you probably want to leave this set as True. If your server already has an SSL certificate installed (i.e.: it accepts https requests), set this to False.
         - with_secret_token: Leave it as True if you want Telegram to send a secret token to be sent in a header "X-Telegram-Bot-Api-Secret-Token" in every webhook request it posts to your server. This header is useful to ensure that the request comes from a webhook set by you. If True, this library will generate one automatically using the token_urlsafe method from python's in-built secrets module and then store it in telepybot_server.json. If you want to define a custom secret (however this is discouraged), just pass a string to this argument (it will also be stored in telepybot_server.json). If you do this, please note that the secret token you choose has to be 1-256 characters long and can only contain characters A-Z, a-z, 0-9, _ and -.
        """

        if isinstance(with_secret_token, str):
            secret = with_secret_token
            if len(secret) == 0 or len(secret) > 256:
                raise Exception('Secret must be between 1 and 256 characters long.')
            for c in secret:
                if c not in BASE64_ALPHABET_URLSAFE:
                    raise Exception('Only characters A-Z, a-z, 0-9, _ and - are allowed for the secret.')
        elif with_secret_token == True:
            secret = token_urlsafe(256)
        
        try:
            with open('telepybot_server.json', 'r', encoding='utf-8') as f:
                telepybot_server_data = json.load(f)
        except:
            telepybot_server_data = {}
        with open('telepybot_server.json', 'w', encoding='utf-8') as f:
            telepybot_server_data["secret"] = secret
            json.dump(telepybot_server_data, f)

        public_ip = get_public_external_ip()
        
        if use_self_signed_certificate == True:
            print("A self signed certificate will be created. Let's configure it! 👇")
            bot_name = input(' - Enter a name for your bot. It will be used in the SSL certificate: ')
            print(' - Where is your server located?')
            server_location = ServerLocationInfo(
                country=input(' --> Country (2 letter code. i.e.: use AR for Argentina): '),
                state=input(' --> State: '),
                city=input(' --> City: ')
            )
            self.ssl.generate_certificate(
                public_ip=public_ip,
                bot_name=bot_name,
                location=server_location
            )
            cert = self.ssl.pubkey_bytes
        else:
            cert = None

        resp = self.set(
            public_ip=public_ip,
            webhook_location=webhook_location,
            secret_token=secret,
            public_certificate=cert
        )
        if resp == True:
            print('Webhook was set correctly.')
        # if not, the self.set() function already raises an error.
