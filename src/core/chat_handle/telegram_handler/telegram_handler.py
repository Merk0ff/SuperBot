import logging
import requests
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
        """Send text message.
                    Send text message using chat api
                    Args:
                        user_id: user/chat id where to send.
                        text: text to send
                    Returns:
                        Status code
                 """
        try:
            self.bot.send_message(user_id, text)
            return 200
        except Exception as e:
            logging.error(str(e))
            return -1

    def receive_text(self, callback):
        """Receive text message decorator.
                    Receive text message using chat api than call callback
                    Args:
                        callback: callback function that will be called after receive.
                    Returns:
                        self
         """
        @self.bot.message_handler(content_types=['text'])
        def receive_message(message):
            callback(message.chat.id, message.text)
            return receive_message

    def receive_file(self, callback):
        """Receive message with file decorator.
                    Receive message with file chat api than call callback
                    Args:
                        callback: callback function that will be called after receive.
                    Returns:
                        self
         """

        @self.bot.message_handler(content_types=['document'])
        def receive_file_msg(message):
            callback(message.chat.id, message.document)
            return receive_file_msg

    def receive_voice(self, callback):
        """Receive voice message decorator.
                    Receive voice message api than call callback
                    Args:
                        callback: callback function that will be called after receive.
                    Returns:
                        self
         """

        @self.bot.message_handler(content_types=['voice'])
        def receive_voice_msg(msg):
            file_info = self.bot.get_file(msg.voice.file_id)
            file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(self.TOKEN, file_info.file_path))
            callback(msg.chat.id, file.content)
            return receive_voice_msg

    def send_meme(self, meme):
        """Send meme message.
                    Send meme image message using chat api
                    Args:
                        meme: meme image.
                    Returns:
                        Status code
         """
        pass

    def run(self):
        """Start receiving messages.
                    Args:
                        None.
                    Returns:
                        None
         """
        self.bot.polling()
