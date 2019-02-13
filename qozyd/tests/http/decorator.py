from unittest import TestCase

from qozyd.http import Request, HttpException
from qozyd.http.decorator import json_response, json_validate
from qozyd.http.response import JsonResponse, Response
from qozyd.utils.json import JsonSchema


class NonDefaultJsonSerializableClass():
    def __json__(self):
        return {
            "type": "NonDefaultJsonSerializableClass"
        }


class TestJsonResponse(TestCase):
    def test_json_response_string(self):
        @json_response
        def method():
            return "string"

        response = method()

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.content, "\"string\"")

    def test_json_response_non_default_serializable_object(self):
        @json_response
        def method():
            return NonDefaultJsonSerializableClass()

        response = method()

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.content, "{\"type\": \"NonDefaultJsonSerializableClass\"}")

    def test_use_existing_response(self):
        existing_response = Response("test", "text/plain")

        @json_response
        def method():
            return existing_response

        response = method()

        self.assertIs(response, existing_response)


class TestJsonValidate(TestCase):
    def test_no_validate(self):
        class TestController():
            @json_validate({})
            def method(self, request):
                return True

        controller = TestController()

        self.assertTrue(controller.method(Request("POST", "/", {}, {}, "{}")))
        self.assertTrue(controller.method(Request("POST", "/", {}, {}, "\"test\"")))

    def test_validity(self):
        class TestController():
            @json_validate(JsonSchema.number(minimum=0, maximum=10))
            def method(self, request):
                return True

        controller = TestController()

        with self.assertRaises(HttpException):
            controller.method(Request("POST", "/", {}, {}, "\"string-not-number\""))

        self.assertTrue(controller.method(Request("POST", "/", {}, {}, "5")))
