from abc import ABCMeta, abstractmethod

__author__ = "Dukshtau Philip"
__copyright__ = "Copyright 2019, The Project#1"
__credits__ = ["Dukshtau Philip"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Dukshtau Philip"
__email__ = "f.dukshtau@gmail.com"
__status__ = "develop"


class ChatHandle:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_text(self, message):
        """Send text message.
            Send text message using chat api
            Args:
                message: text to send.
            Returns:
                Status code
         """
        pass

    @abstractmethod
    def receive_text(self, callback):
        """Receive text message decorator.
            Receive text message using chat api than call callback
            Args:
                callback: callback function that will be called after receive.
            Returns:
                self
         """
        pass
        # def receive_decorator(*args, **kwargs):
        #     callback()
        #
        # return receive_decorator

    @abstractmethod
    def receive_file(self, callback):
        """Receive message with file decorator.
            Receive message with file chat api than call callback
            Args:
                callback: callback function that will be called after receive.
            Returns:
                self
         """
        pass

    @abstractmethod
    def send_meme(self, meme):
        """Send meme message.
            Send meme image message using chat api
            Args:
                meme: meme image.
            Returns:
                Status code
         """
        pass

    @abstractmethod
    def receive_voice(self, callback):
        """Receive voice message decorator.
            Receive voice message api than call callback
            Args:
                callback: callback function that will be called after receive.
            Returns:
                self
         """
        pass
