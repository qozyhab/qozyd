from qozyd.http import Router
from qozyd.services.service_container import Instance
from qozyd.context import HttpContext


class PluginContextBuilder():
    def services(self):
        pass

    def routes(self):
        pass

    def create(self, app_root, base_path="/", parent_context=None):
        plugin_services = (Instance(app_root, name="plugin_root"),)
        plugin_services += tuple(self.services() or ())

        plugin_router = Router(self.routes() or ())

        return HttpContext(plugin_services, router=plugin_router, base_path=base_path, parent=parent_context)
