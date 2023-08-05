from abc import ABC, abstractmethod

from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage


class PyNetgamesServerListener(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def receive_connection_success(self):
        raise NotImplementedError("Method receive_disconnect not overwritten")

    @abstractmethod
    def receive_match(self, match: MatchStartedMessage):
        raise NotImplementedError("Method match_started not overwritten")

    @abstractmethod
    def receive_move(self, match: MoveMessage):
        raise NotImplementedError("Method receive_move not overwritten")

    @abstractmethod
    def receive_error(self, error: Exception):
        pass

    @abstractmethod
    def receive_disconnect(self):
        raise NotImplementedError("Method receive_disconnect not overwritten")

    def receive_match_requested_success(self):
        pass

    def receive_move_sent_success(self):
        pass
