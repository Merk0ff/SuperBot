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

# Set up logger
logging.basicConfig(filename="debug.log", level=logging.INFO)


class DialogFlow(NLPHandle):
    def __init__(self,  token):
        """Init.
             Init DialogFlow class
             Args:
                 token: Dialog flow token.
             Returns:
                 None.
          """
        self.token = token
        self.request_text = apiai.ApiAI(token).text_request()

        self.request_text.lang = 'ru'

    def send_text_to_nlp(self, text_to_send, user_id):
        """Send text message to nlp platform.
            Send text message to nlp platform using nlp api
            Args:
                text_to_send: text to send.
                user_id: user_id to handle session
            Returns:
                Dict with paced text
         """
        self.request_text.session_id = str(user_id)
        self.request_text.query = text_to_send

        response_dict = dict

        try:
            response_dict = json.loads(self.request_text.getresponse().read().decode('utf-8'))
        except Exception as e:
            logging.error(str(e))

        return response_dict

    def send_voice_to_nlp(self, voice_to_send):
        """Send voice message to nlp platform.
            Send voice message to nlp platform using nlp api
            Args:
                voice_to_send: voice to send.
            Returns:
                Dict with paced voice
         """
        pass
