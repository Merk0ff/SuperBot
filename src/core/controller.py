# from src.core.chat_handle import ChatHandle
from src.core.nlp_handle.dialogflow_handler.dialogflow_handler import  DialogFlow

__author__ = "Dukshtau Philip"
__copyright__ = "Copyright 2019, The Project#1"
__credits__ = ["Dukshtau Philip"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Dukshtau Philip"
__email__ = "f.dukshtau@gmail.com"
__status__ = "develop"

# Chat handle instance
chatHandle = object

# NLP handle instance
nlpHandle = object


def set_up(config):
    """Set up some parameters.
        Args:
            config: Dict with tokens and so on.
        Returns:
            None.
     """
    # chatHandle = ChatHandle(config['dialogflow_api_token'])
    nlpHandle = DialogFlow(config['dialogflow_api_token'])
