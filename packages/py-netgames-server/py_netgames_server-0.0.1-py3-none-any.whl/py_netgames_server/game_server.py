import dataclasses
import logging
from logging import Logger
from typing import Type, Dict, Callable, TypeVar, Set, Awaitable

from py_netgames_model.messaging.message import MatchRequestMessage, Message, MatchStartedMessage, MoveMessage
from websockets import WebSocketServerProtocol

from py_netgames_server.match import Match

T = TypeVar('T', bound=Message)


class GameServer:
    _matches: Set[Match]
    _handle_map: Dict[Type[T], Callable[[T, WebSocketServerProtocol], Awaitable[None]]]
    _logger: Logger

    def __init__(self):
        super().__init__()
        self._matches = set()
        self._handle_map = {
            MatchRequestMessage: self._start_match,
            MoveMessage: self._move
        }
        self._logger = logging.getLogger("py_netgames_server")

    async def handle_message(self, message: Message, sender: WebSocketServerProtocol):
        self._logger.debug(f"Handling message {message}")
        await self._handle_map[message.__class__](message, sender)

    async def handle_disconnect(self, disconnected_socket: WebSocketServerProtocol):
        try:
            match = next(match for match in self._matches if disconnected_socket in match.players)
            [await websocket.close(reason="Player disconnected") for websocket in match.players - {disconnected_socket}]
            if match in self._matches:
                self._matches.remove(match)
            self._logger.debug(f"Dropped match with {len(match.players)} connections after player disconnected.")
        except StopIteration:
            self._logger.debug(f"No match found for disconnected websocket.")

    async def _start_match(self, message: MatchRequestMessage, sender: WebSocketServerProtocol):
        try:
            existing_match = next(match for match in self._matches if match.accepting_players(message.game_id))
            self._matches.remove(existing_match)
            match = dataclasses.replace(existing_match, players=frozenset([*existing_match.players, sender]))
            self._matches.add(match)
            if not match.accepting_players(message.game_id):
                [await self._send(MatchStartedMessage(match.id, position), {websocket}) for position, websocket in
                 enumerate(match.players)]
        except StopIteration:
            match = Match.create(message, sender)
            self._matches.add(match)

    async def _move(self, message: MoveMessage, sender: WebSocketServerProtocol):
        try:
            match = next(match for match in self._matches if match.id == message.match_id)
            await self._send(message, match.players - {sender})
        except StopIteration:
            self._logger.error(f"Match not found for match_id {message.match_id}")

    async def _send(self, message: Message, recipients: [WebSocketServerProtocol]):
        [await websocket.send(message.to_payload().to_json()) for websocket in recipients]
