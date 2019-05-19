import logging
import weakref
from functools import partial

from aiohttp import web, WSCloseCode
from qozyd.context import AsyncContextExecutable

from qozyd.controller import Controller
from qozyd.models import Qozy
from qozyd.utils.json import json_decode, json_encode


logger = logging.getLogger(__name__)


class ChannelWebsocketController(Controller, AsyncContextExecutable):
    def __init__(self, app_root: Qozy):
        self.root = app_root
        self.websockets = weakref.WeakSet()

    async def stop(self):
        for websocket in set(self.websockets):
            await websocket.close(code=WSCloseCode.GOING_AWAY, message="Server shutdown")

    async def channel_websocket(self, request):
        websocket = web.WebSocketResponse()
        await websocket.prepare(request)

        self.websockets.add(websocket)

        subscriptions = {}

        async def channel_changed(channel, value, old_value):
            await websocket.send_str(json_encode({
                "type": "update",
                "payload": {
                    "thing_id": channel.thing.id,
                    "channel_name": channel.name,
                    "value": value,
                    "old_value": old_value
                }
            }))

        try:
            async for message in websocket:
                if message.type == web.WSMsgType.TEXT:
                    command = json_decode(message.data)

                    if command["type"] == "subscribe":
                        thing_id = command["payload"]["thing_id"]
                        channel_name = command["payload"]["channel_name"]

                        channel_id = (thing_id, channel_name)
                        channel = self.root[thing_id].channel(channel_name)

                        if not channel_id in subscriptions:
                            callback = partial(channel_changed, channel)
                            channel.on_change.append(callback)

                            subscriptions[channel_id] = callback

                        await websocket.send_str(json_encode({
                            "type": "update",
                            "payload": {
                                "thing_id": channel.thing.id,
                                "channel_name": channel.name,
                                "value": channel.value,
                                "old_value": None
                            }
                        }))
                    elif command["type"] == "unsubscribe":
                        thing_id = command["payload"]["thing_id"]
                        channel_name = command["payload"]["channel_name"]

                        channel_id = (thing_id, channel_name)

                        if channel_id in subscriptions:
                            channel = self.root[thing_id].channel(channel_name)

                            channel.on_change.remove(subscriptions[channel_id])
                            del subscriptions[channel_id]
                    elif command["type"] == "clear":
                        # todo: clear alle subscriptions
                        pass
                elif message.type == web.WSMsgType.ERROR:
                    logger.info(f"Websocket connection closed with exception {str(websocket.exception())}")
        finally:
            self.websockets.discard(websocket)

        logger.info("Websocket connection closed")

        # remove all channel subscription
        for channel_id, callback in subscriptions.items():
            thing_id, channel_name = channel_id
            channel = self.root[thing_id].channel(channel_name)

            channel.on_change.remove(callback)

        return websocket

    def routes(self):
        return [
            web.get("/api/channels/ws", self.channel_websocket)
        ]
