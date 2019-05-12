from aiohttp import web

from qozyd import VERSION
from qozyd.controller import Controller
from qozyd.http.decorator import json_response


class QozyController(Controller):
    @json_response
    async def info(self, request):
        return {
            "version": VERSION
        }

    def routes(self):
        return [
            web.get("/api", self.info)
        ]
