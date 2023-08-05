import asyncio

import websockets
from py_netgames_model.messaging.deserializer import WebhookPayloadDeserializer
from websockets import WebSocketServerProtocol, ConnectionClosedError
from websockets.legacy.server import WebSocketServer

from py_netgames_server.game_server import GameServer


class WebSocketServerBuilder:
    _deserializer: WebhookPayloadDeserializer
    _server: GameServer

    def __init__(self) -> None:
        super().__init__()
        self._deserializer = WebhookPayloadDeserializer()
        self._server = GameServer()

    async def async_serve(self, port=8765) -> WebSocketServer:
        return await websockets.serve(self.listen, "localhost", port)

    def serve(self, port):
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.listen, "localhost", port))
        asyncio.get_event_loop().run_forever()

    async def listen(self, websocket: WebSocketServerProtocol):
        try:
            async for message in websocket:
                await self._server.handle_message(self._deserializer.deserialize(message), websocket)
            await self._server.handle_disconnect(websocket)
        except ConnectionClosedError:
            await self._server.handle_disconnect(websocket)
