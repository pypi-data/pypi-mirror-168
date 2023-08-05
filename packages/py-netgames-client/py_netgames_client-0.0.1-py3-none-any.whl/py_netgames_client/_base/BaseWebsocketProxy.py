import asyncio
import logging
import threading
import warnings
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from concurrent.futures import Future
from typing import Optional, Dict
from uuid import UUID

from py_netgames_model.messaging.deserializer import WebhookPayloadDeserializer
from py_netgames_model.messaging.message import MoveMessage, MatchRequestMessage, MatchStartedMessage
from py_netgames_model.messaging.webhook_payload import WebhookPayloadType
from py_netgames_server.websocket_server_builder import WebSocketServerBuilder
from websockets import client, WebSocketClientProtocol

from py_netgames_client.id.IdentifierFileGenerator import IdentifierFileGenerator


class BaseWebsocketProxy(ABC):
    _thread: threading.Thread
    _loop: AbstractEventLoop
    _websocket: Optional[WebSocketClientProtocol]
    _deserializer: WebhookPayloadDeserializer
    _game_id: UUID
    _logger: logging.Logger

    def __init__(self, game_id: UUID = None) -> None:
        super().__init__()
        self._logger = logging.getLogger("py_netgames_client")
        self._loop = asyncio.new_event_loop()
        self.__deserializer = WebhookPayloadDeserializer()
        self._game_id = game_id if game_id else IdentifierFileGenerator().get_or_create_identifier()
        self._logger.info(
            f"Game identified by game_id: {self._game_id}."
            f" Different instances of the same game must use the same game_id id in order to have matches.")
        self._websocket = None

        def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = threading.Thread(target=start_background_loop, args=(self._loop,))
        self._thread.setDaemon(True)
        self._thread.start()

    def send_connect(self, address: str = "localhost:8765", run_server_when_connection_refused: bool = True) -> None:

        if not isinstance(address, str):
            return warnings.warn(self._invalid_type_message(address, "address", "send_connect", "str"), stacklevel=2)

        if not isinstance(run_server_when_connection_refused, bool):
            return warnings.warn(
                self._invalid_type_message(run_server_when_connection_refused, "run_server_when_connection_refused",
                                           "send_connect", "bool"), stacklevel=2)

        if self._open():
            return self._logger.debug(f"Call to send_connect when connection is already active.", stacklevel=2)

        async def async_connect():

            async def attempt_connection(url):
                self._websocket = await client.connect("ws://" + url)
                self._listen()
                self._connection_success()

            try:
                await attempt_connection(address)
            except ConnectionRefusedError as connection_refused_error:
                if run_server_when_connection_refused:
                    try:
                        logging.getLogger("websockets.server").addFilter(
                            lambda record: logging.getLogger().level <= logging.DEBUG)
                        await WebSocketServerBuilder().async_serve()
                        await attempt_connection("localhost:8765")
                    except Exception as e:
                        return self._error(e)
                else:
                    return self._error(connection_refused_error)
            except Exception as e:
                return self._error(e)

        self._run(target=async_connect)

    def send_match(self, amount_of_players: int) -> None:

        if not isinstance(amount_of_players, int):
            return warnings.warn(
                self._invalid_type_message(amount_of_players, "amount_of_players", "send_match", "int"),
                stacklevel=2)

        if self._closed():
            return warnings.warn(f"Call to send_match when there is no active connection", stacklevel=2)

        self._send(MatchRequestMessage(self._game_id, amount_of_players).to_payload().to_json(),
                   self._match_requested_success)

    def send_move(self, match_id: UUID, payload: Dict[str, any]) -> None:

        if not isinstance(match_id, UUID):
            return warnings.warn(
                f"Invalid value {match_id} supplied as parameter match_id in call to send_move."
                f" match_id should be the value received on match start (receive_match)",
                stacklevel=2)

        payload_type_description = "a dict with string keys and any permutation of the following basic types as values:" \
                                   " dict, list, tuple, str, int, float, bool, None"

        if not isinstance(payload, dict):
            return warnings.warn(self._invalid_type_message(payload, "payload", "send_move", payload_type_description),
                                 stacklevel=2)

        if self._closed():
            return warnings.warn(f"Call to send_move when there is no active connection", stacklevel=2)

        try:
            move_message = MoveMessage(match_id, payload).to_payload().to_json()
        except TypeError as type_error:
            self._logger.error(type_error)
            return warnings.warn(
                f"Error when serializing supplied payload {payload}." f" payload should be a {payload_type_description}",
                stacklevel=2)

        self._send(move_message, self._move_sent_success)

    def send_disconnect(self) -> None:

        if self._closed():
            return self._logger.debug(f"Call to send_disconnect when there is no active connection", stacklevel=2)

        async def async_disconnect():
            try:
                await self._websocket.close()
                return self._disconnection()
            except Exception as e:
                return self._error(e)

        self._run(target=async_disconnect)

    @abstractmethod
    def _receive_match_start(self, match: MatchStartedMessage):
        raise NotImplementedError()

    @abstractmethod
    def _receive_move(self, move: MoveMessage):
        raise NotImplementedError()

    @abstractmethod
    def _disconnection(self):
        raise NotImplementedError()

    @abstractmethod
    def _connection_success(self):
        raise NotImplementedError()

    @abstractmethod
    def _error(self, error: Exception):
        raise NotImplementedError()

    @abstractmethod
    def _match_requested_success(self):
        raise NotImplementedError()

    @abstractmethod
    def _move_sent_success(self):
        raise NotImplementedError()

    def _send(self, message: str, on_success) -> None:
        async def async_send():
            try:
                await self._websocket.send(message)
                return on_success()
            except Exception as e:
                return self._error(e)

        self._run(target=async_send)

    def _listen(self) -> None:
        async def async_listen():
            try:
                async for message in self._websocket:
                    message = self.__deserializer.deserialize(message)
                    self._logger.debug(f"Message received: {message}")
                    if WebhookPayloadType.MATCH_STARTED == message.type():
                        self._receive_match_start(message)
                    elif WebhookPayloadType.MOVE == message.type():
                        self._receive_move(message)
                self._disconnection()
            except Exception as e:
                return self._error(e)

        self._run(target=async_listen)

    def _open(self):
        return self._websocket and self._websocket.open

    def _closed(self):
        return not self._open()

    def _invalid_type_message(self, value: any, parameter_name: str, method_name: str, actual_type: str) -> str:
        return f"Invalid value {value} supplied as parameter {parameter_name} in call to {method_name}." \
               f" {parameter_name} expects a {actual_type}"

    def _run(self, target) -> Future:
        return asyncio.run_coroutine_threadsafe(target(), self._loop)
