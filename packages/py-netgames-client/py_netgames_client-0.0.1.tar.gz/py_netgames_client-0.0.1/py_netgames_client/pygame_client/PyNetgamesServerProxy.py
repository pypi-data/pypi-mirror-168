import pygame
from py_netgames_model.messaging.message import MoveMessage, MatchStartedMessage

from py_netgames_client._base.BaseWebsocketProxy import BaseWebsocketProxy

CONNECTED = pygame.event.custom_type()
CONNECTION_ERROR = pygame.event.custom_type()
MATCH_STARTED = pygame.event.custom_type()
MATCH_REQUESTED = pygame.event.custom_type()
MOVE_SENT = pygame.event.custom_type()
MOVE_RECEIVED = pygame.event.custom_type()
DISCONNECTED = pygame.event.custom_type()


class PyNetgamesServerProxy(BaseWebsocketProxy):
    _pygame: pygame

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._pygame = pygame

    def _receive_match_start(self, match: MatchStartedMessage):
        pygame.event.post(pygame.event.Event(MATCH_STARTED, message=match))

    def _receive_move(self, move: MoveMessage):
        pygame.event.post(pygame.event.Event(MOVE_RECEIVED, message=move))

    def _disconnection(self):
        pygame.event.post(pygame.event.Event(DISCONNECTED, message={}))

    def _connection_success(self):
        pygame.event.post(pygame.event.Event(CONNECTED, message={}))

    def _error(self, error: Exception):
        pygame.event.post(pygame.event.Event(CONNECTION_ERROR, message=error))

    def _match_requested_success(self):
        pygame.event.post(pygame.event.Event(MATCH_REQUESTED, message={}))

    def _move_sent_success(self):
        pygame.event.post(pygame.event.Event(MOVE_SENT, message=MATCH_REQUESTED))
