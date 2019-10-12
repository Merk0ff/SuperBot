import logging
import telebot
from telebot import apihelper
from src.core.chat_handle.chat_handle_abc import ChatHandle

# Set up logger
logging.basicConfig(filename="text.log", level=logging.INFO)

# Add proxy, slava ros com nadzoru!
apihelper.proxy = {'https': 'https://165.22.44.147:80'}


class TelegramBot(ChatHandle):

    def __init__(self, token):
        self.TOKEN = token
        self.bot = telebot.TeleBot(token)

    def send_text(self, user_id, text):
        try:
            self.bot.send_message(user_id, text)
            return 200
        except Exception as e:
            logging.error(str(e))
            return -1

    def receive_text(self, callback):
        @self.bot.message_handler(content_types=['text'])
        def receive_message(message):
            callback(message.chat.id, message.text)
            return receive_message

    def receive_file(self, callback):
        pass

    def receive_voice(self, callback):
        pass

    def send_meme(self, meme):
        pass

    def run(self):
        self.bot.polling()
