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


def json_result(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        return json.dumps(func(*args, **kwargs), cls=JsonEncoder)

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
    def type(cls, type, title=None, description=None, default=None, examples=None):
        result = {
            "type": type
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
    def string(cls, title=None, description=None, default=None, examples=None):
        return cls.type("string", title=title, description=description, default=default, examples=examples)

    @classmethod
    def integer(cls, minimum=None, maximum=None, title=None, description=None, default=None, examples=None):
        result = cls.type("integer", title=title, description=description, default=default, examples=examples)

        if minimum:
            result["minimum"] = minimum

        if maximum:
            result["maximum"] = maximum

        return result

    @classmethod
    def number(cls, minimum=None, maximum=None, title=None, description=None, default=None, examples=None):
        result = cls.type("number", title=title, description=description, default=default, examples=examples)

        if minimum:
            result["minimum"] = minimum

        if maximum:
            result["maximum"] = maximum

        return result

    @classmethod
    def array(cls, items, title=None, description=None, default=None, examples=None):
        result = cls.type("array", title=title, description=description, default=default, examples=examples)
        result["items"] = items

        return result


class ChannelSchema():
    BASE_CHANNEL_SCHEMA = JsonSchema.object(
        properties=JsonSchema.properties(
            channel=JsonSchema.string(title="Channel name"),
        )
    )

    SWITCH_CHANNEL_SCHEMA = JsonSchema.extend(
        BASE_CHANNEL_SCHEMA,
        title="Switch",
        properties=JsonSchema.properties(
            type=JsonSchema.const("Switch"),
        )
    )

    STRING_CHANNEL_SCHEMA = JsonSchema.extend(
        BASE_CHANNEL_SCHEMA,
        title="String",
        properties=JsonSchema.properties(
            type=JsonSchema.const("String"),
        )
    )

    NUMBER_CHANNEL_SCHEMA = JsonSchema.extend(
        BASE_CHANNEL_SCHEMA,
        title="Number",
        properties=JsonSchema.properties(
            type=JsonSchema.const("Number"),
            min=JsonSchema.number(title="Min"),
            max=JsonSchema.number(title="Max"),
            step=JsonSchema.number(title="Step"),
        )
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
