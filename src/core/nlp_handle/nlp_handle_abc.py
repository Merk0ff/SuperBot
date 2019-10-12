from abc import ABCMeta, abstractmethod

__author__ = "Dukshtau Philip"
__copyright__ = "Copyright 2019, The Project#1"
__credits__ = ["Dukshtau Philip"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Dukshtau Philip"
__email__ = "f.dukshtau@gmail.com"
__status__ = "develop"


class NLPHandle:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_text_to_nlp(self, user_id, text_to_send):
        """Send text message to nlp platform.
            Send text message to nlp platform using nlp api
            Args:
                text_to_send: text to send.
                user_id: user_id to handle session
            Returns:
                Dict with paced text
         """
        pass

    @abstractmethod
    def send_voice_to_nlp(self, voice_to_send):
        """Send voice message to nlp platform.
            Send voice message to nlp platform using nlp api
            Args:
                voice_to_send: voice to send.
            Returns:
                Dict with paced voice
         """
        pass
