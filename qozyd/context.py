import asyncio

from qozyd.controller import Controller
from qozyd.services.service_container import ServiceContainer, Instance


class ContextExecutable():
    def start(self):
        raise NotImplementedError()

    def stop(self):
        pass


class AsyncContextExecutable():
    async def start(self):
        raise NotImplementedError()

    async def stop(self):
        pass


class Context():
    def __init__(self, services, parent=None):
        self.service_container = ServiceContainer(
            (Instance(self, name="context"),) + services
        )
        self.parent = parent

        self.tasks = {}

    def start(self):
        self.service_container.start()

        for name, service in self.service_container.services.items():
            if isinstance(service, ContextExecutable):
                service.start()
            elif isinstance(service, AsyncContextExecutable):
                self.tasks[name] = asyncio.create_task(service.start())

        return self

    def stop(self):
        for name, service in self.service_container.services.items():
            if isinstance(service, ContextExecutable):
                service.stop()
            elif isinstance(service, AsyncContextExecutable):
                service.stop()

                self.tasks[name].cancel()

        return self


class HttpContext(Context):
    def __init__(self, app, services, parent=None):
        super().__init__(services, parent=parent)

        self.app = app

    def start(self):
        super().start()

        # register controllers
        for service in self.service_container.services.values():
            if isinstance(service, Controller):
                self.app.add_routes(service.routes())

        return self
