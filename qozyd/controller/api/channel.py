from aiohttp import web

from qozyd.controller import Controller
from qozyd.http.decorator import json_response
from qozyd.models import Qozy
from qozyd.models.bridges.exceptions import OfflineException
from qozyd.models.channels import ColorChannel
from qozyd.utils.color import RGB, HSV, HSL


class ChannelController(Controller):
    COLOR_TYPES = {
        "rgb": RGB,
        "hsv": HSV,
        "hsl": HSL,
    }

    def __init__(self, app_root: Qozy, bridge_manager):
        self.root = app_root
        self.bridge_manager = bridge_manager

    @json_response
    async def get(self, request):
        thing_id = request.match_info.get("thing_id")
        channel_name = request.match_info.get("channel_name")

        return self.root[thing_id].channel(channel_name).value()

    @json_response
    async def set(self, request):
        thing_id = request.match_info.get("thing_id")
        channel_name = request.match_info.get("channel_name")

        thing = self.root[thing_id]
        channel = thing.channel(channel_name)

        value = await request.json()

        if isinstance(channel, ColorChannel):
            color_type = value["type"]
            color_value = value["value"]

            value = self.COLOR_TYPES[color_type](*color_value)

        try:
            return await self.bridge_manager.apply(thing, channel, value)
        except OfflineException:
            return False

    @json_response
    async def on(self, request):
        thing_id = request.match_info.get("thing_id")
        channel_name = request.match_info.get("channel_name")

        return self.root[thing_id].channel(channel_name).on()

    @json_response
    async def off(self, request):
        thing_id = request.match_info.get("thing_id")
        channel_name = request.match_info.get("channel_name")

        return self.root[thing_id].channel(channel_name).off()

    @json_response
    async def toggle(self, request):
        thing_id = request.match_info.get("thing_id")
        channel_name = request.match_info.get("channel_name")

        return self.root[thing_id].channel(channel_name).toggle()

    def routes(self):
        return [
            web.put("/api/things/{thing_id}/channels/{channel_name}", self.set),
            web.put("/api/things/{thing_id}/channels/{channel_name}/on", self.on),
            web.put("/api/things/{thing_id}/channels/{channel_name}/off", self.off),
            web.put("/api/things/{thing_id}/channels/{channel_name}/toggle", self.toggle)
        ]
