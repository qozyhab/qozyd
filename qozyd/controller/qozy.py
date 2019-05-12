from aiohttp import web

from qozyd.controller import Controller, static_file_handler


class QozyController(Controller):
    def routes(self):
        return [
            web.route("*", "/{path:.*}",
                      static_file_handler(package="qozyd", base_path="web/dist", directory_index="index.html"))
        ]
