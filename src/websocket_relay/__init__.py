# SPDX-FileCopyrightText: 2023-present Filip Strajnar <filip.strajnar@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from pprint import pprint
from falcon.asgi import App, Request
from falcon.asgi.ws import WebSocket

_all_clients: dict[str, dict[str, list[WebSocket]]] = {}


class WebSocketRelay:

    async def on_websocket(self, _: Request, ws: WebSocket, type: str,
                           address: str, action: str):

        await ws.accept()

        # Ensure there is action dictionary for address.
        if address not in _all_clients:
            _all_clients[address] = dict()

        actions_at_address = _all_clients[address]

        # Ensure there is list of clients for this action.
        if action not in actions_at_address:
            actions_at_address[action] = list()

        # Subscribe the client.
        clients = actions_at_address[action]
        clients.append(ws)

        # Forward data to all that are subscribed.
        while ws.ready:
            if type == "binary":
                data = await ws.receive_data()

                for client in _all_clients[address][action]:
                    # Don't send back to the sender, and only send to clients that are ready
                    if client != ws and client.ready:
                        await client.send_data(data)

            if type == "text":
                data = await ws.receive_text()

                for client in _all_clients[address][action]:
                    # Don't send back to the sender, and only send to clients that are ready
                    if client != ws and client.ready:
                        await client.send_text(data)

        await ws.close()


relay = App()
# Type can be either text or binary
relay.add_route('/{type}/{address}/{action}', WebSocketRelay())
