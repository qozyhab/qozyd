from aiohttp import web

from qozyd.services.service_container import Instance
from qozyd.context import HttpContext, Context


class PluginContextBuilder():
    def services(self):
        return tuple()

    def create(self, app_root, parent_context: Context = None) -> HttpContext:
        app = web.Application()

        plugin_services = (Instance(app_root, name="plugin_root"),)
        plugin_services += tuple(self.services() or ())

        return HttpContext(app, plugin_services, parent=parent_context)
