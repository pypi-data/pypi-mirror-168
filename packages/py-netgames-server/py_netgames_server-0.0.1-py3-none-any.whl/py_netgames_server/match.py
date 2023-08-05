from dataclasses import dataclass, field
from typing import FrozenSet
from uuid import UUID, uuid4

from py_netgames_model.messaging.message import MatchRequestMessage
from websockets import WebSocketServerProtocol


@dataclass(eq=True, frozen=True)
class Match:
    game_id: UUID
    id: UUID = field(default_factory=uuid4)
    amount_of_players: int = field(default_factory=lambda: 2)
    players: FrozenSet[WebSocketServerProtocol] = field(default_factory=frozenset)

    @classmethod
    def create(cls, message: MatchRequestMessage, websocket: WebSocketServerProtocol):
        return Match(game_id=message.game_id, amount_of_players=message.amount_of_players,
                     players=frozenset([websocket]))

    def accepting_players(self, game_id: UUID) -> bool:
        return game_id == self.game_id and len(self.players) < self.amount_of_players
