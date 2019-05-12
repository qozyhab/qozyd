import uuid
import logging

from aiohttp import web
from aiohttp.web_request import Request

from qozyd.controller import Controller
from qozyd.http.decorator import json_response
from qozyd.http.utils import get_or_404
from qozyd.models.bridges import Bridge

logger = logging.getLogger(__name__)


class BridgeController(Controller):
    def __init__(self, app_root, plugin_manager, bridge_manager, transaction_manager):
        self.root = app_root
        self.plugin_manager = plugin_manager
        self.bridge_manager = bridge_manager
        self.transaction_manager = transaction_manager

    @json_response
    async def bridges(self, request):
        expand = request.query.getone("expand", False)

        if expand:
            return dict(self.root.bridges)

        return list(self.root.bridges.keys())

    @json_response
    async def bridge(self, request):
        bridge_id = request.match_info.get("bridge_id")

        return get_or_404(self.root.bridges, bridge_id)

    @json_response
    async def running(self, request):
        bridge_id = request.match_info.get("bridge_id")

        bridge = self.root.bridges[bridge_id]

        return self.bridge_manager.is_active(bridge)

    @json_response
    async def remove(self, request):
        bridge_id = request.match_info.get("bridge_id")

        with self.transaction_manager:
            self.root.delete_bridge(self.root.bridges[bridge_id])

        return True

    @json_response
    async def things(self, request):
        bridge_id = request.match_info.get("bridge_id")

        return dict(self.root.bridges[bridge_id].things)

    @json_response
    async def types(self, request):
        return list(self.plugin_manager.bridge_plugins().keys())

    @json_response
    async def add(self, request: Request):
        bridge_type = await request.json()

        bridge_class = self.plugin_manager.bridge_class(bridge_type)
        bridge = Bridge(str(uuid.uuid4()), bridge_class)

        with self.transaction_manager:
            logging.info("Adding bridge of type {} with id {}".format(bridge_type, bridge.id))
            self.root.add_bridge(bridge)

        return bridge.id

    @json_response
    async def settings_set(self, request):
        bridge_id = request.match_info.get("bridge_id")

        settings = await request.json()

        with self.transaction_manager:
            result = self.root.bridges[bridge_id].set_settings(settings)

        return result

    @json_response
    async def deactivate(self, request):
        bridge_id = request.match_info.get("bridge_id")
        bridge = get_or_404(self.root.bridges, bridge_id)

        with self.transaction_manager:
            bridge.active = False

        return True

    @json_response
    async def activate(self, request):
        bridge_id = request.match_info.get("bridge_id")
        bridge = get_or_404(self.root.bridges, bridge_id)

        with self.transaction_manager:
            bridge.active = True

        return True

    def routes(self):
        return [
            web.get("/api/bridges", self.bridges),
            web.get("/api/bridges/types", self.types),
            web.post("/api/bridges", self.add),
            web.get("/api/bridges/{bridge_id}", self.bridge),
            web.post("/api/bridges/{bridge_id}/activate", self.activate),
            web.post("/api/bridges/{bridge_id}/deactivate", self.deactivate),
            web.get("/api/bridges/{bridge_id}/running", self.running),
            web.delete("/api/bridges/{bridge_id}", self.remove),
            web.get("/api/bridges/{bridge_id}/things", self.things),
            web.put("/api/bridges/{bridge_id}/settings", self.settings_set)
        ]
