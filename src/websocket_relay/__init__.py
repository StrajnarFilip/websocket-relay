# SPDX-FileCopyrightText: 2023-present Filip Strajnar <filip.strajnar@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from pprint import pprint
from falcon.asgi import App, Request
from falcon.asgi.ws import WebSocket


class WebSocketRelay:

    def __init__(self) -> None:
        super().__init__()
        self._all_clients: dict[str, dict[str, list[WebSocket]]] = {}

    def _ensure_structure(self, address: str, action: str):
        # Ensure there is action dictionary for address.
        if address not in self._all_clients:
            self._all_clients[address] = dict()

        actions_at_address = self._all_clients[address]

        # Ensure there is list of clients for this action.
        if action not in actions_at_address:
            actions_at_address[action] = list()

    async def _send_binary(self, ws: WebSocket, clients: list[WebSocket]):
        data = await ws.receive_data()

        for client in clients:
            # Don't send back to the sender, and only send to clients that are ready
            if client != ws and client.ready:
                await client.send_data(data)

    async def _send_text(self, ws: WebSocket, clients: list[WebSocket]):
        data = await ws.receive_text()

        for client in clients:
            # Don't send back to the sender, and only send to clients that are ready
            if client != ws and client.ready:
                await client.send_text(data)

    async def on_websocket(self, _: Request, ws: WebSocket, type: str,
                           address: str, action: str):
        await ws.accept()

        self._ensure_structure(address, action)

        # Subscribe the client.
        clients = self._all_clients[address][action]
        clients.append(ws)

        # Forward data to all that are subscribed.
        while ws.ready:
            if type == "binary":
                await self._send_binary(ws, clients)

            if type == "text":
                await self._send_text(ws, clients)

        await ws.close()


relay = App()
# Type can be either text or binary
relay.add_route('/{type}/{address}/{action}', WebSocketRelay())
