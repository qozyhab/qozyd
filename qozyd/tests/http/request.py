from unittest import TestCase

from qozyd.http import Bag, Request


class BagTest(TestCase):
    def test_get_bool(self):
        bag = Bag()
        bag["key"] = "1"
        self.assertTrue(bag.get_bool("key"))

        bag = Bag()
        bag["key"] = ["0", "1"]
        self.assertTrue(bag.get_bool("key"))

        bag = Bag()
        bag["key"] = "false"
        self.assertFalse(bag.get_bool("key"))

        bag = Bag()
        self.assertTrue(bag.get_bool("key", True))

    def test_get_number(self):
        bag = Bag()
        bag["key"] = "123"
        self.assertEqual(bag.get_number("key"), 123)

        bag = Bag()
        bag["key"] = "123.12"
        self.assertEqual(bag.get_number("key"), 123.12)

        bag = Bag()
        bag["key"] = ["123.12", "512"]
        self.assertEqual(bag.get_number("key"), 512)

        bag = Bag()
        self.assertEqual(bag.get_number("key", 987), 987)


class RequestTest(TestCase):
    def test_request_json(self):
        request = Request("GET", "/", {}, {}, None)
        with self.assertRaises(TypeError):
            request.request_json()

        request = Request("GET", "/", {}, {}, "\"json-string\"")
        self.assertEqual(request.request_json, "json-string")
