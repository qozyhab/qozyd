from datetime import datetime
from unittest import TestCase

from qozyd.utils.json import JsonSchema, JsonEncoder, json_result, ChannelSchema


class TestJsonEncodableObject():
    def __init__(self, val):
        self.val = val

    def __json__(self):
        return {
            "val": self.val
        }


class TestNotJsonEncodableObject():
    def __init__(self, val):
        self.val = val


class JsonEncoderTest(TestCase):
    def test_encode(self):
        self.assertEqual(
            JsonEncoder().default(TestJsonEncodableObject("test")),
            {
                "val": "test"
            }
        )

        self.assertEqual(
            JsonEncoder().default({1, 2, 3}),
            [1, 2, 3]
        )

        now = datetime.now()
        self.assertEqual(
            JsonEncoder().default(now),
            now.isoformat()
        )

        with self.assertRaises(TypeError):
            JsonEncoder().default(TestNotJsonEncodableObject("test"))


class JsonResponseTest(TestCase):
    def test_json_response(self):
        @json_result
        def function():
            return "string"

        result = function()
        self.assertEqual(result, "\"string\"")


class JsonSchemaTest(TestCase):
    def test_type(self):
        self.assertEqual(JsonSchema.type("string", title="test-title"), {"type": "string", "title": "test-title"})
        self.assertEqual(JsonSchema.type("string", title="test-title", description="test-description"),
                         {"type": "string", "title": "test-title", "description": "test-description"})
        self.assertEqual(JsonSchema.type("string", title="test-title", description="test-description", default="default-value"),
                         {"type": "string", "title": "test-title", "description": "test-description",
                          "default": "default-value"})
        self.assertEqual(JsonSchema.type("string", title="test-title", description="test-description", default="default-value",
                                           examples=["example-1", "example-2"]),
                         {"type": "string", "title": "test-title", "description": "test-description",
                          "default": "default-value", "examples": ["example-1", "example-2"]})

    def test_string(self):
        self.assertEqual(JsonSchema.string(), {"type": "string"})

    def test_integer(self):
        self.assertEqual(JsonSchema.integer(), {"type": "integer"})
        self.assertEqual(JsonSchema.integer(minimum=1), {"type": "integer", "minimum": 1})
        self.assertEqual(JsonSchema.integer(minimum=1, maximum=10), {"type": "integer", "minimum": 1, "maximum": 10})

    def test_number(self):
        self.assertEqual(JsonSchema.number(), {"type": "number"})
        self.assertEqual(JsonSchema.number(minimum=1), {"type": "number", "minimum": 1})
        self.assertEqual(JsonSchema.number(minimum=1, maximum=10), {"type": "number", "minimum": 1, "maximum": 10})

    def test_array(self):
        self.assertEqual(JsonSchema.array(JsonSchema.string()), {"type": "array", "items": {"type": "string"}})

    def test_const(self):
        self.assertEqual(JsonSchema.const("CONSTANT-VALUE"), {"const": "CONSTANT-VALUE"})

    def test_properties(self):
        self.assertEqual(
            JsonSchema.properties(username=JsonSchema.string(), password=JsonSchema.string()),
            {
                "username": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
            }
        )

    def test_object(self):
        self.assertEqual(
            JsonSchema.object(
                JsonSchema.properties(username=JsonSchema.string(), password=JsonSchema.string()),
                required=["username"]
            ),
            {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                },
                "required": ["username"],
                "additionalProperties": False
            }
        )

    def test_extend(self):
        object_schema = JsonSchema.object(
            JsonSchema.properties(username=JsonSchema.string(), password=JsonSchema.string()),
            required=["username"]
        )

        self.assertEqual(
            object_schema,
            {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                },
                "required": ["username"],
                "additionalProperties": False
            }
        )

        self.assertEqual(
            JsonSchema.extend(object_schema, properties=JsonSchema.properties(age=JsonSchema.integer())),
            {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                    "age": {
                        "type": "integer"
                    }
                },
                "required": ["username"],
                "additionalProperties": False
            }
        )

        self.assertEqual(
            JsonSchema.extend(object_schema, required=["password"]),
            {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                },
                "required": ["username", "password"],
                "additionalProperties": False
            }
        )

        self.assertEqual(
            JsonSchema.extend(object_schema, title="User"),
            {
                "type": "object",
                "title": "User",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                },
                "required": ["username"],
                "additionalProperties": False
            }
        )

        self.assertEqual(
            JsonSchema.extend(object_schema, description="Description for User object"),
            {
                "type": "object",
                "description": "Description for User object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                },
                "required": ["username"],
                "additionalProperties": False
            }
        )

        self.assertEqual(
            JsonSchema.extend(object_schema, default={"username": "NewUser"}),
            {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                },
                "required": ["username"],
                "default": {"username": "NewUser"},
                "additionalProperties": False
            }
        )

        self.assertEqual(
            JsonSchema.extend(object_schema, examples=[{"username": "NewUser"}, {"username": "User", "password": "Pass"}]),
            {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                },
                "required": ["username"],
                "examples": [{"username": "NewUser"}, {"username": "User", "password": "Pass"}],
                "additionalProperties": False
            }
        )

    def test_one_of(self):
        self.assertEqual(
            JsonSchema.one_of(JsonSchema.string(), JsonSchema.integer()),
            {
                "oneOf": [
                    {"type": "string"},
                    {"type": "integer"},
                ]
            }
        )

    def test_any_of(self):
        self.assertEqual(
            JsonSchema.any_of(JsonSchema.string(), JsonSchema.integer()),
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "integer"},
                ]
            }
        )


class ChannelSchemaTest(TestCase):
    maxDiff = None
    def test_all(self):
        self.assertDictEqual(
            ChannelSchema.all(),
            JsonSchema.any_of(
                ChannelSchema.SWITCH_CHANNEL_SCHEMA,
                ChannelSchema.STRING_CHANNEL_SCHEMA,
                ChannelSchema.NUMBER_CHANNEL_SCHEMA,
            )
        )

    def test_for_types(self):
        self.assertEqual(
            ChannelSchema.for_types(["String"]),
            JsonSchema.any_of(
                ChannelSchema.STRING_CHANNEL_SCHEMA,
            )
        )

        self.assertEqual(
            ChannelSchema.for_types(["String", "Switch"]),
            JsonSchema.any_of(
                ChannelSchema.STRING_CHANNEL_SCHEMA,
                ChannelSchema.SWITCH_CHANNEL_SCHEMA,
            )
        )

        self.assertEqual(
            ChannelSchema.for_types(["String", "Switch"], extend_all={
                "properties": JsonSchema.properties(
                    new_prop=JsonSchema.string(),
                )
            }),
            JsonSchema.any_of(
                JsonSchema.extend(ChannelSchema.STRING_CHANNEL_SCHEMA, properties=JsonSchema.properties(new_prop=JsonSchema.string())),
                JsonSchema.extend(ChannelSchema.SWITCH_CHANNEL_SCHEMA, properties=JsonSchema.properties(new_prop=JsonSchema.string())),
            )
        )

        self.assertEqual(
            ChannelSchema.for_types(["String", "Switch"], extend={
                "Switch": {
                    "properties": JsonSchema.properties(
                        new_prop=JsonSchema.string(),
                    )
                }
            }),
            JsonSchema.any_of(
                ChannelSchema.STRING_CHANNEL_SCHEMA,
                JsonSchema.extend(ChannelSchema.SWITCH_CHANNEL_SCHEMA, properties=JsonSchema.properties(new_prop=JsonSchema.string())),
            )
        )
