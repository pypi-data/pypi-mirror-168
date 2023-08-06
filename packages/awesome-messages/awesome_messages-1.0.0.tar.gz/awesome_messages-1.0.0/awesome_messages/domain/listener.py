from abc import ABC, abstractmethod

from .handler import MessageHandler


class MessageListener(ABC):

    @abstractmethod
    def start_listening(self):
        pass

    @abstractmethod
    def stop_listening(self):
        pass

    @abstractmethod
    def add_handler(self, handler: MessageHandler):
        pass
