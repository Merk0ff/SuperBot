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


def voice(id, voice, **kwargs):
    resp = nlpHandle.send_voice_to_nlp(voice, id)
    handler_receive(resp, id, **kwargs)


def receiver(id, text, **kwargs):
    resp = nlpHandle.send_text_to_nlp(text, id)
    handler_receive(resp, id, **kwargs)


def handler_receive(resp, id, **kwargs):
    if 'answer' in resp:
        chatHandle.send_msg(id, resp['answer'])
    elif resp['intent'] == "Когда зарплата":
        username = "@" + kwargs['user_id']
        user = dbHandle.get_user_by_username(username)
        if user:
            msg = "зарплата будет " + user.salary_date.strftime("%d") + " числа"
        else:
            msg = "Ты кто такой?"
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
            chatHandle.send_msg(resp.user_id, "Молодец! Взял книгу!")
        elif resp.action == "вернуть":
            dbHandle.return_book(resp.book_id)
            chatHandle.send_msg(resp.user_id, "Молодец! Вернул книгу!")
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
