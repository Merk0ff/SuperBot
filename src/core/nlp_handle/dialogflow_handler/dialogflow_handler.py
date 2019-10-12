import apiai
import json
import logging
from src.core.nlp_handle.nlp_handle_abc import NLPHandle

__author__ = "Dukshtau Philip"
__copyright__ = "Copyright 2019, The Project#1"
__credits__ = ["Dukshtau Philip"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Dukshtau Philip"
__email__ = "f.dukshtau@gmail.com"
__status__ = "develop"

# setup logger
logging.basicConfig(filename="debug.log", level=logging.INFO)


class DialogFlow(NLPHandle):
    def __init__(self,  token):
        self.token = token
        self.request_text = apiai.ApiAI(token).text_request()

        self.request_text.lang = 'ru'

    def send_text_to_nlp(self, text_to_send, user_id):
        self.request_text.session_id = str(user_id)
        self.request_text.query = text_to_send

        try:
            response_json = json.loads(self.request_text.getresponse().read().decode('utf-8'))
        except Exception as e:
            logging.error(str(e))

        return response_json

    def send_voice_to_nlp(self, voice_to_send):
        pass
