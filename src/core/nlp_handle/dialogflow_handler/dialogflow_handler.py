# import dialogflow_v2 as dialogflow
import os
import logging
import urllib
import json
import apiai
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
IAM_TOKEN = 'CggaATEVAgAAABKABIQhLt2D0GoulRwpUZx4NlKsRWGoAYfuSmLpltLFYTF0wcpY3XyXLfaWCUsZt3EznXBQhC6lBY9S3rqlFn38xLUTpZrv4ouN2nPoIvMujmFEfS_0avqyh6xdtkknfLhrjuDm7JqeqXS6794k7tQ5_u3oSOl8_rc0g58HbPtBFhWvJxe3LnlW5Z_aJLDgVF5rRh3ocE2qYFHIycqh55YXBmCvTRwqTEJQkdzNdVFdCCS0ECQr1pxvI1ix5F-cUID6Njcj024fjT-tG7TkdKGj3OW7L2QA9AlD2QGJFHZE4qP5pOVeHqh3kHyee5l9dZrURPnUTDHAa0OqSXwKqJLooZkDP-rTe56P-aFwTOF5Kjl3HwQbdyNe5OneXEz_UGBVOgjB-OC1JNtqsiNplgsVmOGK1mNxdA_Y0dfX_EiekrI51UHpI1uRCNuxTi-SVkKsKsmZYaZ34cMJFdlvdOo7yGy9Ra-WidDGRt6-sW2xd77YBDYSNW8L4aO61BnVL7EMC6eURd6ef8ml1MTgle3mMmXyt1EnrAjoB6uejPhzIR6qylGXCVQzqhkBwhQAT8vZc2fl-Q1hlyxuZ9dxtORFLi9cGYTY1bJCPvEk1BtxHaGPDWLdqChCp8mPvSRHlqnmUz7mNStvPlQXWcrOdhtVrB3kop2TvVSJ3KqCJjx5VP1KGmEKIGY5ZGFjNWE1ZWVjZjQ1ZjI4MGRmZjk5YjQyMmEwYTZhEO22i-0FGK2Iju0FIh8KFGFqZWNtaWlwbXI5aWRhMGtkcDFmEgdGaWwwMDkxWgAwAjgBSggaATEVAgAAAFABIPAE'


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
                        Dict with paced intent type and paranms or fail str
                        intent - type of intent
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
                            - <Книги>
                                - bookName // Name of the book
                                - author   // Author name
                                - any      // Not full search request just try to find
                                - time     // Count of books to get default = 1
                                - action   // Action with book
                 """
        self.request_text.session_id = str(user_id)
        self.request_text.query = text_to_send

        response = dict

        try:
            response = json.loads(self.request_text.getresponse().read().decode('utf-8'))
        except Exception as e:
            logging.error(str(e))
            return 'fail'

        response_dict = \
        {
            'intent': response['result']['metadata']['intentName'],
            'params': []
        }

        for key, value in response['result']['parameters'].items():
            if value:
                response_dict['params'].append({key: value})

        return response_dict

    @staticmethod
    def __speech_to_text__(voice):

        params = "&".join([
            "topic=general",
            "folderId=%s" % "b1g5l8jlg5vlc8hj4f0g",
            "lang=ru-RU"
        ])

        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=voice)
        url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

        response_data = urllib.request.urlopen(url).read().decode('UTF-8')
        decoded_data = json.loads(response_data)

        return decoded_data['result']

    def send_voice_to_nlp(self, voice_to_send, user_id):
        """Send voice message to nlp platform.
            Send voice message to nlp platform using nlp api
            Args:
                voice_to_send: voice to send.
            Returns:
                Dict with paced text
                intent - type of intent
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
                    - <Книги>
                        - bookName // Name of the book
                        - author   // Author name
                        - any      // Not full search request just try to find
                        - time     // Count of books to get default = 1
                        - action   // Action with book

         """

        text = self.__speech_to_text__(voice_to_send)

        response_dict = self.send_text_to_nlp(text, user_id)

        return response_dict
