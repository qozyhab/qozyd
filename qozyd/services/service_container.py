import logging
from collections import namedtuple

from logdecorator import log_on_start, log_on_error

from qozyd.utils import import_symbol


logger = logging.getLogger(__name__)


class ServiceNotFoundException(Exception):
    def __init__(self, service_name):
        super().__init__("Service \"{:s}\" not found".format(service_name))
        self.service_name = service_name


class Definition():
    def __init__(self, name):
        self.name = name


class Instance(Definition):
    def __init__(self, obj, name):
        super().__init__(name)

        self.obj = obj


class Service(Definition):
    def __init__(self, cls, name, inject=None):
        super().__init__(name)

        self.cls = cls
        self.inject = inject or ()


Reference = namedtuple("Reference", ["service_name"])


class ServiceContainer():
    def __init__(self, service_definitions):
        self.service_definitions = service_definitions

        self.services = {
            "service_container": self
        }

    def _has_own_service(self, service_name):
        return service_name in self.services

    def get(self, name):
        if name in self.services:
            return self.services[name]
        
        try:
            if self._has_own_service("context"):
                context = self.get("context")

                if context.parent:
                    return context.parent.service_container.get(name)
        except ServiceNotFoundException:
            pass

        raise ServiceNotFoundException("Service \"{:s}\" not found".format(name))

    @log_on_start(logging.INFO, "Creating Service \"{service_definition.name:s}\"")
    @log_on_error(logging.CRITICAL, "Could not create Service \"{service_definition.name:s}\", required Service \"{e.service_name:s}\" not found.", on_exceptions=ServiceNotFoundException, reraise=True)
    def _create_instance(self, service_definition):
        service_cls = service_definition.cls

        if isinstance(service_cls, str):
            service_cls = import_symbol(service_definition.cls)

        service_args = []

        for injection in service_definition.inject:
            if isinstance(injection, Reference):
                injection = self.get(injection.service_name)
            
            service_args.append(injection)

        service_instance = service_cls(*service_args)

        return service_instance

    def start(self):
        for service_definition in self.service_definitions:
            if isinstance(service_definition, Service):
                service = self._create_instance(service_definition)

                self.services[service_definition.name] = service
            elif isinstance(service_definition, Instance):
                self.services[service_definition.name] = service_definition.obj
            else:
                raise Exception("Unknown service_definition type ({:s}). Instance of {:s} given.".format(str(service_definition), str(service_definition.__class__)))
