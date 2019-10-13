import dialogflow_v2 as dialogflow
import base64
import os
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

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'selectel-inside-bot-dc7da6e2a9d2.json'


class DialogFlow(NLPHandle):
    def __init__(self,  token):
        """Init.
             Init DialogFlow class
             Args:
                 token: Dialog flow token.
             Returns:
                 None.
          """
        self.DIALOGFLOW_PROJECT_ID = 'selectel-inside-bot-vqfdsy'

        self.token = token
        self.session_client = dialogflow.SessionsClient()

    def send_text_to_nlp(self, text_to_send, user_id):
        """Send text message to nlp platform.
            Send text message to nlp platform using nlp api
            Args:
                text_to_send: text to send.
                user_id: user_id to handle session
            Returns:
                Dict with paced text
                instance - type of instance
                params:
                    - <Когда зарплата>:
                        - salary // question about salary
                        - date // asking salary date
                    - <Челик>
                        - last-name // last name of person
                        - given-name // List of person names
                        - aboutPerson // direct question about person
                            - <должность>
                            - <отдел>
                            - <отпуск>
         """
        session = self.session_client.session_path(self.DIALOGFLOW_PROJECT_ID, user_id)

        text_input = dialogflow.types.TextInput(text=text_to_send, language_code='ru')
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = object

        try:
            response = self.session_client.detect_intent(session=session, query_input=query_input) # .query_result.parameters
        except Exception as e:
            logging.error(str(e))
            exit(-1)

        response_dict = \
            {
                'instance': response.query_result.intent.display_name,
                'params': response.query_result.parameters
            }

        return response_dict

    def send_voice_to_nlp(self, voice_to_send, user_id):
        """Send voice message to nlp platform.
            Send voice message to nlp platform using nlp api
            Args:
                voice_to_send: voice to send.
            Returns:
                Dict with paced voice
         """

        encoded_voice = base64.b64encode(voice_to_send)

        audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_OGG_OPUS
        sample_rate_hertz = 16000

        session = self.session_client.session_path(self.DIALOGFLOW_PROJECT_ID, user_id)

        audio_config = dialogflow.types.InputAudioConfig(
            audio_encoding=audio_encoding, language_code='ru',
            sample_rate_hertz=sample_rate_hertz)

        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        response = self.session_client.detect_intent(
            session=session, query_input=query_input,
            input_audio=encoded_voice, timeout=10)

        return response

        pass
