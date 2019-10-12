import logging
import telebot
from src.core.chat_handle.chat_handle_abc import ChatHandle

logging.basicConfig(filename="text.log", level=logging.INFO)


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
        @self.bot.message_handler(commands=['text'])
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
