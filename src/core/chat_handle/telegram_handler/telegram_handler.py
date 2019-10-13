import logging
import requests
import telebot
import requests
import io
from telebot import apihelper
from core.chat_handle.chat_handle_abc import ChatHandle

# Set up logger
logging.basicConfig(filename="text.log", level=logging.INFO)

IAM_TOKEN = 'CggaATEVAgAAABKABIQhLt2D0GoulRwpUZx4NlKsRWGoAYfuSmLpltLFYTF0wcpY3XyXLfaWCUsZt3EznXBQhC6lBY9S3rqlFn38xLUTpZrv4ouN2nPoIvMujmFEfS_0avqyh6xdtkknfLhrjuDm7JqeqXS6794k7tQ5_u3oSOl8_rc0g58HbPtBFhWvJxe3LnlW5Z_aJLDgVF5rRh3ocE2qYFHIycqh55YXBmCvTRwqTEJQkdzNdVFdCCS0ECQr1pxvI1ix5F-cUID6Njcj024fjT-tG7TkdKGj3OW7L2QA9AlD2QGJFHZE4qP5pOVeHqh3kHyee5l9dZrURPnUTDHAa0OqSXwKqJLooZkDP-rTe56P-aFwTOF5Kjl3HwQbdyNe5OneXEz_UGBVOgjB-OC1JNtqsiNplgsVmOGK1mNxdA_Y0dfX_EiekrI51UHpI1uRCNuxTi-SVkKsKsmZYaZ34cMJFdlvdOo7yGy9Ra-WidDGRt6-sW2xd77YBDYSNW8L4aO61BnVL7EMC6eURd6ef8ml1MTgle3mMmXyt1EnrAjoB6uejPhzIR6qylGXCVQzqhkBwhQAT8vZc2fl-Q1hlyxuZ9dxtORFLi9cGYTY1bJCPvEk1BtxHaGPDWLdqChCp8mPvSRHlqnmUz7mNStvPlQXWcrOdhtVrB3kop2TvVSJ3KqCJjx5VP1KGmEKIGY5ZGFjNWE1ZWVjZjQ1ZjI4MGRmZjk5YjQyMmEwYTZhEO22i-0FGK2Iju0FIh8KFGFqZWNtaWlwbXI5aWRhMGtkcDFmEgdGaWwwMDkxWgAwAjgBSggaATEVAgAAAFABIPAE'

# Add proxy, slava ros com nadzoru!
apihelper.proxy = {'https': 'https://167.71.59.12:80'}


class TelegramBot(ChatHandle):

    def __init__(self, token):
        self.TOKEN = token
        self.bot = telebot.TeleBot(token)
        self.send_flag = 1

    @staticmethod
    def synthesize(text):
        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        headers = {
            'Authorization': 'Bearer ' + IAM_TOKEN,
        }

        data = {
            'text': text,
            'lang': 'ru-RU',
            'folderId': "b1g5l8jlg5vlc8hj4f0g",
            'speed': "1",
            'emotion': 'neutral',
            "voice": "oksana"
        }

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

            return resp.content
            # for chunk in resp.iter_content(chunk_size=None):
            #     yield chunk

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

    def send_voice(self, id, voice):
        try:
            self.bot.send_voice(id, voice)
            return 200
        except Exception as e:
            logging.error(str(e))
            return -1

    def send_msg(self, id, *args):
        if self.send_flag == 0:
            self.send_text(id, args[0])
        elif self.send_flag == 1:
            voice = self.synthesize(args[0])
            self.send_voice(id, voice)

    def receive_command(self):
        @self.bot.message_handler(commands=['flag'])
        def change_flag(msg):
            self.send_flag = not self.send_flag

        @self.bot.message_handler(commands=['meme'])
        def change_flag(msg):
            self.send_meme(msg.chat.id)

    def receive_text(self, callback, **kwargs):
        """Receive text message decorator.
                    Receive text message using chat api than call callback
                    Args:
                        callback: callback function that will be called after receive.
                    Returns:
                        self
         """

        @self.bot.message_handler(content_types=['text'])
        def receive_message(message):
            callback(message.chat.id, message.text, user_id=message.from_user.username)
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

    def receive_voice(self, callback, **kwargs):
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
            callback(msg.chat.id, file.content, user_id=msg.from_user.username)
            return receive_voice_msg

    def send_meme(self, user_id):
        """Send meme message.
                    Send meme image message using chat api
                    Args:
                        meme: meme image.
                    Returns:
                        Status code
         """

        # @self.bot.message_handler(commands=['meme'])
        # def send_very_funny_meme(msg):
        # header = {"Accept: application/json"}
        # response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'}).json()
        try:
            response = requests.get("https://meme-api.herokuapp.com/gimme").json()
            meme_url = response['url']
            meme_pic = requests.get(meme_url)
            # img = open("meme.png", "wb")
            # img.write(meme_pic.content)
            # img.close()
            meme = io.BytesIO(meme_pic.content)
            # meme = open("meme.png", "rb")
            self.bot.send_photo(user_id, meme)
        except Exception as e:
            logging.error(str(e))

    def run(self):
        """Start receiving messages.
               Args:
                   None.
               Returns:
                   None
         """
        # self.receive_command()
        self.bot.polling()
