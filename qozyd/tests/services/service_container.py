from qozyd.services.service_container import ServiceContainer, Service, Instance, Prototype, Reference, ServiceNotFoundException
from unittest import TestCase


class ServiceClass():
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return "ServiceClass({:s})".format(str(self.arg))

    def __repr__(self):
        return "ServiceClass({:s})".format(repr(self.arg))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.arg == other.arg


class ServiceContainerTest(TestCase):
    def setUp(self):
        self.service_container = ServiceContainer(
            (
                Instance(ServiceClass("A preinstanced String"), "instance_string_service"),
                Service(ServiceClass, "new_string_service", inject=("An one time on-start created instance",)),

                Service(str, "prototype_argument_string", inject=("An string service to use as injection argument for another service",)),
                Prototype(ServiceClass, "prototype_string_service", inject=(Reference("prototype_argument_string"),))
            )
        )
        self.service_container.start()

    def test_get(self):
        self.assertEqual(self.service_container.get("instance_string_service"), ServiceClass("A preinstanced String"))
        self.assertEqual(self.service_container.get("new_string_service"), ServiceClass("An one time on-start created instance"))
        self.assertEqual(self.service_container.get("prototype_string_service"), ServiceClass("An string service to use as injection argument for another service"))

        self.assertIs(self.service_container.get("instance_string_service"), self.service_container.get("instance_string_service"))
        self.assertIs(self.service_container.get("new_string_service"), self.service_container.get("new_string_service"))

        # Any call to "service_container.get()" will create a new instance of "Prototype" services, so the instances must not be the same
        self.assertIsNot(self.service_container.get("prototype_string_service"), self.service_container.get("prototype_string_service"))

    def test_service_not_found(self):
        with self.assertRaises(ServiceNotFoundException):
            self.service_container.get("unknown_service")

    def tearDown(self):
        self.service_container.stop()
