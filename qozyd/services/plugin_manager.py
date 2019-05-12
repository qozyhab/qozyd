from aiohttp import web

from qozyd.context import ContextExecutable

import pkg_resources


class PluginManager(ContextExecutable):
    PLUGIN_ENTRYPOINT = "qozy.plugin"
    BRIDGE_PLUGIN_ENTRYPOINT = "qozy.bridge"

    def __init__(self, app: web.Application, app_root, transaction_manager, service_container, context):
        self.app = app
        self.app_root = app_root
        self.transaction_manager = transaction_manager
        self.service_container = service_container
        self.context = context

        self.plugin_contexts = {}

    def bridge_plugins(self):
        plugins = {
            entry_point.name: entry_point.load()
            for entry_point
            in pkg_resources.iter_entry_points(self.BRIDGE_PLUGIN_ENTRYPOINT)
        }

        return plugins

    def bridge_class(self, name):
        return self.bridge_plugins()[name]

    def plugins(self):
        plugins = {
            entry_point.name: entry_point.load()
            for entry_point
            in pkg_resources.iter_entry_points(self.PLUGIN_ENTRYPOINT)
        }

        return plugins

    def plugin_context(self, plugin):
        return self.plugin_contexts[plugin]

    def start(self):
        for plugin_name, plugin_class in self.plugins().items():
            plugin = plugin_class()

            with self.transaction_manager:
                plugin_store = self.app_root.get_or_create_plugin_store(plugin_name)

            base_path = "/plugins/{:s}".format(plugin_name)

            plugin_context = plugin.create(plugin_store, parent_context=self.context)

            self.plugin_contexts[plugin_name] = plugin_context

            plugin_context.start()

            self.app.add_subapp(base_path, plugin_context.app)

    def stop(self):
        for plugin_context in self.plugin_contexts.values():
            plugin_context.stop()
