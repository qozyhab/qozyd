from io import BytesIO

from unittest import TestCase
from unittest.mock import Mock

from qozyd.context import Context, HttpContext, UnfittableException
from qozyd.http import Route, Router, Request, NotFoundException, http_server_handler_factory
from qozyd.services.service_container import ServiceContainer, Instance, ServiceNotFoundException


class ContextTest(TestCase):
    def test_context(self):
        context = Context(tuple())

        self.assertIsInstance(context.service_container, ServiceContainer)

    def test_start(self):
        context = Context(tuple())

        self.assertIs(context.start(), context)

        self.assertIs(context.service_container.get("context"), context)

    def test_stop(self):
        context = Context(tuple())
        context.start()

        self.assertIs(context.stop(), context)

    def test_parent(self):
        parent_context = Context(
            (
                Instance("Test String", "string-instance"),
            )
        )
        parent_context.start()

        context = Context(tuple(), parent=parent_context)
        context.start()

        self.assertIs(context.parent, parent_context)

        # Test get service from parent context
        self.assertEqual(context.service_container.get("string-instance"), "Test String")

        with self.assertRaises(ServiceNotFoundException):
            context.service_container.get("non-existing-service")


class HttpContextTest(TestCase):
    def test_handle(self):
        controller = Mock()
        controller.action = Mock(return_value=None)

        context = HttpContext(
            (
                Instance(controller, "controller"),
            ),
            Router(
                (Route(r"^/$", ("controller", "action")),)
            )
        )
        context.start()

        request = Request("GET", "/", {}, {}, None)
        context.handle(request)
        controller.action.assert_called_with(request)

        with self.assertRaises(NotFoundException):
            request = Request("GET", "/not-found", {}, {}, None)
            context.handle(request)

    def test_fit(self):
        sub_context = HttpContext(
            tuple(),
            Router(tuple()),
            "/sub-context"
        )

        request = Request("GET", "/sub-context", {}, {}, None)
        sub_context_request = sub_context.fit(request)
        self.assertEqual(sub_context_request.path, "/")

        request = Request("GET", "/sub-context/sub-resource", {}, {}, None)
        sub_context_request = sub_context.fit(request)
        self.assertEqual(sub_context_request.path, "/sub-resource")

        with self.assertRaises(UnfittableException):
            request = Request("GET", "/wrong-context/sub-resource", {}, {}, None)
            sub_context.fit(request)

    def test_path(self):
        context = HttpContext(tuple(), Router(tuple()), "/")
        self.assertEqual(context.path, "/")

        sub_context = HttpContext(tuple(), Router(tuple()), "/sub-context", parent=context)
        self.assertEqual(sub_context.path, "/sub-context")

        sub_sub_context = HttpContext(tuple(), Router(tuple()), "/sub-sub-context", parent=sub_context)
        self.assertEqual(sub_sub_context.path, "/sub-context/sub-sub-context")
