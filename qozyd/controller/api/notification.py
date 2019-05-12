import logging

from aiohttp import web
from logdecorator import log_on_start

from qozyd.controller import Controller
from qozyd.http.decorator import json_response


logger = logging.getLogger(__name__)


class NotificationController(Controller):
    def __init__(self, app_root):
        self.root = app_root

    @json_response
    async def notifications(self, request):
        return list(self.root.notifications)

    @json_response
    @log_on_start(logging.INFO, "Removing notification at index {index:d}", logger=logger)
    async def remove(self, request):
        index = int(request.match_info.get("index"))

        notification = self.root.notifications[index]
        self.root.delete_notification(notification)

        return True

    def routes(self):
        return [
            web.get("/api/notifications", self.notifications),
            web.delete("/api/notifications/{index:[1-9][0-9]*}", self.remove),
        ]
