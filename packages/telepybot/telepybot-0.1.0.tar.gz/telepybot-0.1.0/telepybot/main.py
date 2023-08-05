import requests, json
from typing import Union

from telepybot.models import ReplyKeyboardMarkup
from telepybot.types import Dices, ParseModes
from .webhook import Webhook

class Telepybot():
    def __init__(self, token: str, debug_mode: bool = False) -> None:
        self._API_TOKEN = token
        self.debug_mode = debug_mode
    
    @property
    def base_url(self):
        return f'https://api.telegram.org/bot{self._API_TOKEN}'
    
    def _is_request_successful(self, r: requests.Request) -> bool:
        try:
            isOk = r.json()["ok"] == True
            return isOk
        except:
            return False
    
    def escape_special_chars(self, text: str, parse_mode: ParseModes) -> str:
        escaped_text = str(text)
        chars_to_escape = {}
        if parse_mode == "MarkdownV2":
            chars = ['\\', '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            for c in chars:
                chars_to_escape[c] = f'\{c}'
        elif parse_mode == "HTML":
            chars_to_escape["<"] = '&lt;'
            chars_to_escape[">"] = '&gt;'
            chars_to_escape["&"] = '&amp;'
        else:
            raise Exception(f'Parse mode "{parse_mode}" is not supported. Please use "MarkdownV2" or "HTML" instead.')
        for char, escaped_char in chars_to_escape.items():
            escaped_text = escaped_text.replace(char, escaped_char)
        return escaped_text
    
    def sendMsg(self, user_id: str, text: str, max_retries: int = 1, reply_markup: ReplyKeyboardMarkup = None, parse_mode: Union[ParseModes, None] = None):
        url = f'{self.base_url}/sendMessage'
        payload = {
            "chat_id": user_id,
            "text": text
        }
        if parse_mode != None:
            payload["parse_mode"] = parse_mode

        if reply_markup != None:
            json_reply_markup = json.dumps(reply_markup.dict(exclude_none=True))
            payload["reply_markup"] = json_reply_markup
        
        for i in range(max_retries):
            r = requests.get(url, params=payload)
            if self.debug_mode == True:
                print(f"Try nr. {i}. Status: {r.status_code} Response: {r.text}")
            isOk = self._is_request_successful(r)
            if isOk:
                break
        return isOk

    def sendDocument(self, user_id: str, file: bytes, caption: str = "", max_retries: int = 1, parse_mode: Union[ParseModes, None] = None):
        
        # multipart/form-data
        url = f'{self.base_url}/sendDocument'
        payload = {
            "chat_id": user_id,
            "caption": caption
        }
        if parse_mode != None:
            payload["parse_mode"] = parse_mode

        for i in range(max_retries):
            r = requests.post(url, params=payload, files={"document": file})
            if self.debug_mode == True:
                print(f"Try nr. {i}. Status: {r.status_code} Response: {r.text}")
            isOk = self._is_request_successful(r)
            if isOk:
                break
        return isOk

    def sendPhoto(self, user_id: str, pic: Union[bytes, str], caption: str = "", max_retries: int = 1, parse_mode: Union[ParseModes, None] = None):
        url = f'{self.base_url}/sendPhoto'
        payload = {
            "chat_id": user_id,
            "caption": caption
        }

        if parse_mode != None:
            payload["parse_mode"] = parse_mode

        for i in range(max_retries):
            if isinstance(pic, bytes):
                # multipart/form-data
                r = requests.post(url, params=payload, files={"photo": pic})
            elif isinstance(pic, str):
                payload["photo"] = pic
                r = requests.post(url, params=payload)
            else:
                raise TypeError("The picture is not in the correct format. Please use bytes for an actual picture file or a string for a url that points to an image.")
            
            if self.debug_mode == True:
                print(f"Try nr. {i}. Status: {r.status_code} Response: {r.text}")

            isOk = self._is_request_successful(r)
            if isOk:
                break
        return isOk
    
    def sendDice(self, user_id: int, emoji: Dices = "🎲", max_retries: int = 1, reply_markup: ReplyKeyboardMarkup = None):
        url = f'{self.base_url}/sendDice'
        payload = {
            "chat_id": user_id,
            "emoji": emoji
        }

        if reply_markup != None:
            json_reply_markup = json.dumps(reply_markup.dict(exclude_none=True))
            payload["reply_markup"] = json_reply_markup
        
        for i in range(max_retries):
            r = requests.get(url, params=payload)
            if self.debug_mode == True:
                print(f"Try nr. {i}. Status: {r.status_code} Response: {r.text}")
            isOk = self._is_request_successful(r)
            if isOk:
                break
        return isOk
    
    @property
    def webhook(self):
        return Webhook(self.base_url, self.debug_mode)