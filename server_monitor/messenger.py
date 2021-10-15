import telegram
import json
import requests

class Telegram:

    def __init__(self, token):
        self._token = token
        self.bot = telegram.Bot(token)

    def send_message(self, chat_id, msg):
        self.bot.sendMessage(chat_id=chat_id, text=msg)

    def get_info(self):
        url = f'https://api.telegram.org/bot{self._token}/getUpdates'
        return json.loads(requests.get(url).text)