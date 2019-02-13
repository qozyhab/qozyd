from unittest import TestCase

from qozyd.http import Router, Route, Request


class RouterTest(TestCase):
    def test_match(self):
        route_root = Route(r"^/$", ("controller", "action"), method="GET")
        route_parameterized = Route(r"^/(?P<param>.+?)$", ("controller", "action"), method="GET")

        router = Router((
            route_root,
            route_parameterized,
        ))

        request = Request("GET", "/", {}, {}, None)
        route, params, matched_path = router.match(request)
        self.assertIs(route, route_root)
        self.assertEqual(params, {})
        self.assertEqual(matched_path, "/")

        request = Request("GET", "/test", {}, {}, None)
        route, params, matched_path = router.match(request)
        self.assertIs(route, route_parameterized)
        self.assertEqual(params, {"param": "test"})
        self.assertEqual(matched_path, "/test")

        request = Request("POST", "/", {}, {}, None)
        self.assertIsNone(router.match(request))

    def test_add_remove(self):
        router = Router(list())
        self.assertEqual(router.routes, [])

        route = Route(r"^/$", ("controller", "action"), method="GET")
        router.add(route)
        self.assertEqual(router.routes, [route])

        router.remove(route)
        self.assertEqual(router.routes, [])
