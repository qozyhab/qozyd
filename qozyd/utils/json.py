import copy

import json
import functools
from collections import OrderedDict
from datetime import datetime


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__json__"):
            return obj.__json__()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        else:
            return super().default(obj)


def json_encode(obj):
    return json.dumps(obj, cls=JsonEncoder)


def json_decode(string):
    return json.loads(string)


def json_result(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        return json_encode(func(*args, **kwargs))

    return wrapper_func


class JsonSchema():
    @classmethod
    def one_of(cls, *types):
        return {
            "oneOf": list(types)
        }

    @classmethod
    def any_of(cls, *types):
        return {
            "anyOf": list(types)
        }

    @classmethod
    def properties(cls, **properties):
        return {
            property_name: property_value for property_name, property_value in properties.items()
        }

    @classmethod
    def object(cls, properties, required=None, title=None, description=None, default=None, examples=None):
        result = cls.type("object", title=title, description=description, default=default, examples=examples)

        result["properties"] = properties
        if required:
            result["required"] = required

        result["additionalProperties"] = False

        return result

    @classmethod
    def extend(cls, object, properties=None, required=None, title=None, description=None, default=None, examples=None):
        object = copy.deepcopy(object)

        title = title or object.get("title", None)
        if title:
            object["title"] = title

        description = description or object.get("description", None)
        if description:
            object["description"] = description

        default = default or object.get("default", None)
        if default:
            object["default"] = default

        if properties:
            new_properties = object.get("properties", {})
            new_properties.update(properties)

            object["properties"] = new_properties

        if required:
            object["required"] = object.get("required", []) + required

        if examples:
            object["examples"] = object.get("examples", []) + examples

        return object

    @classmethod
    def type(cls, type, nullable=False, title=None, description=None, default=None, examples=None):
        result = {
            "type": type if not nullable else [type, "null"]
        }

        if title:
            result["title"] = title

        if description:
            result["description"] = description

        if default:
            result["default"] = default

        if examples:
            result["examples"] = examples

        return result

    @classmethod
    def const(cls, value):
        return {
            "const": value
        }

    @classmethod
    def string(cls, nullable=False, min_length=None, max_length=None, title=None, description=None, default=None, examples=None):
        result = cls.type("string", nullable=nullable, title=title, description=description, default=default, examples=examples)

        if min_length:
            result["minLength"] = min_length

        if max_length:
            result["maxLength"] = max_length

        return result

    @classmethod
    def integer(cls, nullable=False, minimum=None, maximum=None, title=None, description=None, default=None, examples=None):
        result = cls.type("integer", nullable=nullable, title=title, description=description, default=default, examples=examples)

        if minimum:
            result["minimum"] = minimum

        if maximum:
            result["maximum"] = maximum

        return result

    @classmethod
    def number(cls, nullable=False, minimum=None, maximum=None, title=None, description=None, default=None, examples=None):
        result = cls.type("number", nullable=nullable, title=title, description=description, default=default, examples=examples)

        if minimum:
            result["minimum"] = minimum

        if maximum:
            result["maximum"] = maximum

        return result

    @classmethod
    def array(cls, items, nullable=False, min_items=None, max_items=None, title=None, description=None, default=None, examples=None):
        result = cls.type("array", nullable=nullable, title=title, description=description, default=default, examples=examples)
        result["items"] = items

        if min_items:
            result["minItems"] = min_items

        if max_items:
            result["maxItems"] = max_items

        return result


class ChannelSchema():
    BASE_CHANNEL_SCHEMA = JsonSchema.object(
        properties=JsonSchema.properties(
            channel=JsonSchema.string(title="Channel name", min_length=1),
        ),
        required=["channel",]
    )

    SWITCH_CHANNEL_SCHEMA = JsonSchema.extend(
        BASE_CHANNEL_SCHEMA,
        title="Switch",
        properties=JsonSchema.properties(
            type=JsonSchema.const("Switch"),
        ),
        required=["type",]
    )

    STRING_CHANNEL_SCHEMA = JsonSchema.extend(
        BASE_CHANNEL_SCHEMA,
        title="String",
        properties=JsonSchema.properties(
            type=JsonSchema.const("String"),
        ),
        required=["type",]
    )

    NUMBER_CHANNEL_SCHEMA = JsonSchema.extend(
        BASE_CHANNEL_SCHEMA,
        title="Number",
        properties=JsonSchema.properties(
            type=JsonSchema.const("Number"),
            min=JsonSchema.number(title="Min"),
            max=JsonSchema.number(title="Max"),
            step=JsonSchema.number(title="Step"),
        ),
        required=["type",]
    )

    SCHEMA_BY_TYPE = OrderedDict((
        ("Switch", SWITCH_CHANNEL_SCHEMA),
        ("String", STRING_CHANNEL_SCHEMA),
        ("Number", NUMBER_CHANNEL_SCHEMA),
    ))

    @classmethod
    def for_types(cls, types, extend_all=None, extend=None):
        extend = extend or dict()

        schemas = []

        for type in types:
            schema = cls.SCHEMA_BY_TYPE[type]

            if extend_all:
                schema = JsonSchema.extend(schema, **extend_all)

            if type in extend:
                schema = JsonSchema.extend(schema, **extend[type])

            schemas.append(schema)

        return JsonSchema.any_of(*schemas)

    @classmethod
    def all(cls, extend_all=None, extend=None):
        return cls.for_types(cls.SCHEMA_BY_TYPE.keys(), extend_all=extend_all, extend=extend)
