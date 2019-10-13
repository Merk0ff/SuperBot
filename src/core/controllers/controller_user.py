import requests
from src.core.chat_handle.telegram_handler.telegram_handler import TelegramBot
from src.core.nlp_handle.dialogflow_handler.dialogflow_handler import DialogFlow
from src.core.chat_handle.chat_handle_abc import ChatHandle
from src.core.nlp_handle.nlp_handle_abc import NLPHandle

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

def voice(id, voice):

    resp = nlpHandle.send_voice_to_nlp(voice, id)

def receiver(id, text):
    resp = nlpHandle.send_text_to_nlp(text, id)


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

    chatHandle.receive_text(receiver)
    chatHandle.receive_voice(voice)


def run():
    chatHandle.run()
