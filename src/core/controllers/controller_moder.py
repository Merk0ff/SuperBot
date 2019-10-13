from core.chat_handle.telegram_handler.telegram_handler import TelegramBot
from core.nlp_handle.dialogflow_handler.dialogflow_handler import DialogFlow
from core.chat_handle.chat_handle_abc import ChatHandle
from core.nlp_handle.nlp_handle_abc import NLPHandle

# from src.core.database.db_context import PostgresDbContext

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


# dbHandle = PostgresDbContext(False)


def receiver(id, text):
    resp = nlpHandle.send_text_to_nlp(text, id)
    # handler_receive(resp)
    pass


def voice(id, voice):
    resp = nlpHandle.send_voice_to_nlp(voice, id)
    # handler_receive(resp)


# def handler_receive(resp):
#     if resp.type == "зарплата":
#         msg = "зарплата будет"
#         chatHandle.send_text(resp.user_id, msg)
#     elif resp.type == "сотрудник":
#         msg = dbHandle.get_user()
#         chatHandle.send_text(resp.user_id, msg)
#     elif resp.type == "книга":
#         if resp.action == "взять":
#             dbHandle.rent_book(resp.book_id, resp.user_id)
#             chatHandle.send_text(resp.user_id, "Молодец! Взял книгу!")
#         elif resp.action == "вернуть":
#             dbHandle.return_book(resp.book_id)
#             chatHandle.send_text(resp.user_id, "Молодец! Вернул книгу!")
#         # chatHandle.send_text()
#     elif resp.type == "переговорка":
#         # chatHandle.send_text()
#         pass
#     elif resp.type == "отпуск":
#         # chatHandle.send_text()
#         pass


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
    # chatHandle.send_meme()


def run():
    chatHandle.run()
