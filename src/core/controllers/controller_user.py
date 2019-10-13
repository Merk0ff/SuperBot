import requests
from src.core.chat_handle.telegram_handler.telegram_handler import TelegramBot
from src.core.nlp_handle.dialogflow_handler.dialogflow_handler import DialogFlow
from src.core.chat_handle.chat_handle_abc import ChatHandle
from src.core.nlp_handle.nlp_handle_abc import NLPHandle

from src.core.database.db_context import PostgresDbContext

__author__ = "Dukshtau Philip"
__copyright__ = "Copyright 2019, The Project#1"
__credits__ = ["Dukshtau Philip"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Dukshtau Philip"
__email__ = "f.dukshtau@gmail.com"
__status__ = "develop"

# Chat handle instance
chatHandle = ChatHandle

# NLP handle instance
nlpHandle = NLPHandle

dbHandle = PostgresDbContext(False)
IAM_TOKEN = 'CggaATEVAgAAABKABIQhLt2D0GoulRwpUZx4NlKsRWGoAYfuSmLpltLFYTF0wcpY3XyXLfaWCUsZt3EznXBQhC6lBY9S3rqlFn38xLUTpZrv4ouN2nPoIvMujmFEfS_0avqyh6xdtkknfLhrjuDm7JqeqXS6794k7tQ5_u3oSOl8_rc0g58HbPtBFhWvJxe3LnlW5Z_aJLDgVF5rRh3ocE2qYFHIycqh55YXBmCvTRwqTEJQkdzNdVFdCCS0ECQr1pxvI1ix5F-cUID6Njcj024fjT-tG7TkdKGj3OW7L2QA9AlD2QGJFHZE4qP5pOVeHqh3kHyee5l9dZrURPnUTDHAa0OqSXwKqJLooZkDP-rTe56P-aFwTOF5Kjl3HwQbdyNe5OneXEz_UGBVOgjB-OC1JNtqsiNplgsVmOGK1mNxdA_Y0dfX_EiekrI51UHpI1uRCNuxTi-SVkKsKsmZYaZ34cMJFdlvdOo7yGy9Ra-WidDGRt6-sW2xd77YBDYSNW8L4aO61BnVL7EMC6eURd6ef8ml1MTgle3mMmXyt1EnrAjoB6uejPhzIR6qylGXCVQzqhkBwhQAT8vZc2fl-Q1hlyxuZ9dxtORFLi9cGYTY1bJCPvEk1BtxHaGPDWLdqChCp8mPvSRHlqnmUz7mNStvPlQXWcrOdhtVrB3kop2TvVSJ3KqCJjx5VP1KGmEKIGY5ZGFjNWE1ZWVjZjQ1ZjI4MGRmZjk5YjQyMmEwYTZhEO22i-0FGK2Iju0FIh8KFGFqZWNtaWlwbXI5aWRhMGtkcDFmEgdGaWwwMDkxWgAwAjgBSggaATEVAgAAAFABIPAE'


def synthesize(text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + IAM_TOKEN,
    }

    data = {
        'text': text,
        'lang': 'ru-RU',
        'folderId': "b1g5l8jlg5vlc8hj4f0g",
        'speed': "0.5",
        'emotion': 'evil',
        "voice": "ermil"
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


def voice(id, voice, **kwargs):
    resp = nlpHandle.send_voice_to_nlp(voice, id)
    handler_receive(resp, id)


def receiver(id, text, **kwargs):
    resp = nlpHandle.send_text_to_nlp(text, id)
    handler_receive(resp, id)


def handler_receive(resp, id, username):
    if 'answer' in resp:
        chatHandle.send_text(id, resp['answer'])
    elif resp['intent'] == "Когда зарплата":
        user = dbHandle.get_user_
        msg = "зарплата будет " + user.salary_date + "числа"
        chatHandle.send_msg(id, msg)
    elif resp['intent'] == "Челик":
        user = dbHandle.get_user_by_name(resp['params']['given-name'][0], resp['params']['last-name'])
        if user:
            msg = "Знаю такого!" + user.first_name + \
                  " Тот еще пидор!" + "Это его должность - " \
                  + user.position
        else:
            msg = "Да хуй знает че доебался????"
        chatHandle.send_msg(id, msg)
    elif resp.type == "книга":
        if resp.action == "взять":
            dbHandle.rent_book(resp.book_id, resp.user_id)
            chatHandle.send_text(resp.user_id, "Молодец! Взял книгу!")
        elif resp.action == "вернуть":
            dbHandle.return_book(resp.book_id)
            chatHandle.send_text(resp.user_id, "Молодец! Вернул книгу!")
        # chatHandle.send_text()
    elif resp.type == "переговорка":
        # chatHandle.send_text()
        pass
    elif resp.type == "отпуск":
        # chatHandle.send_text()
        pass


def set_up(config):
    """Set up some parameters.
        Args:
            config: Dict with tokens and so on.
        Returns:
            None.
     """
    global chatHandle
    global nlpHandle

    chatHandle = TelegramBot(config['telegram_api_token'])
    nlpHandle = DialogFlow(config['dialogflow_api_token'])

    chatHandle.receive_command()
    chatHandle.receive_text(receiver)
    chatHandle.receive_voice(voice)


def run():
    chatHandle.run()
    # chatHandle.receive_co
