import inspect
import json
from typing import Dict

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validator_for
from collections import OrderedDict

from qozyd.utils.json import JsonSchema


class Property():
    def __init__(self, name=None, property_name=None, required=True, nullable=False):
        self.required = required
        self.nullable = nullable
        self.name = name
        self.property_name = property_name

    def schema(self, definitions=None):
        raise NotImplementedError

    def _patch(self, data, old_value):
        raise NotImplementedError

    def _api_representation(self, obj):
        raise NotImplementedError


class Field(Property):
    def __init__(self, type, name=None, property_name=None, required=True, nullable=False):
        super().__init__(name=name, property_name=property_name, required=required, nullable=nullable)

        self.type = type

    def schema(self, definitions=None):
        return JsonSchema.type(self.type, nullable=self.nullable)

    def _patch(self, data, old_value):
        return data

    def _api_representation(self, obj):
        return obj


class Const(Field):
    def __init__(self, value, name=None):
        super().__init__(type="string", required=True, name=name, nullable=False)

        self.value = value

    def schema(self, definitions=None):
        return JsonSchema.const(self.value)

    def _patch(self, data, old_value):
        if data != self.value:
            raise Exception(f"Cannot patch Const")

        return data

    def _api_representation(self, obj):
        return self.value


class Integer(Field):
    def __init__(self, name=None, property_name=None, minimum=None, maximum=None, required=True):
        super().__init__(type="integer", name=name, property_name=property_name, required=required)

        self.minimum = minimum
        self.maximum = maximum

    def schema(self, definitions=None):
        return JsonSchema.integer(minimum=self.minimum, maximum=self.maximum)


class Array(Property):
    def __init__(self, type, min_items=None, max_items=None, name=None, property_name=None, required=True):
        super().__init__(required=required, name=name, property_name=property_name)

        self.type = type
        self.min_items = min_items
        self.max_items = max_items

    def schema(self, definitions=None):
        return JsonSchema.array(items=[self.type.schema(definitions)], min_items=self.min_items, max_items=self.max_items)

    def _patch(self, data, old_value):
        result = []

        for array_value in data:
            array_item = self.type._patch(array_value, None)
            result.append(array_item)

        return result

    def _api_representation(self, obj):
        if obj is None:
            return None

        return [
            self.type._api_representation(item)
            for item in obj
        ]


class Relation(Property):
    def __init__(self, target_type, required=True, nullable=False):
        super().__init__(required=required, nullable=nullable)

        self.target_type = target_type

    def schema(self, definitions=None):
        if self.nullable:
            return {
                "anyOf": [
                    {
                        "type": "null"
                    },
                    self.target_type.schema(definitions)
                ]
            }

        return self.target_type.schema(definitions)

    def _patch(self, data, old_value):
        return self.target_type._patch(data, old_value)

    def _api_representation(self, obj):
        if obj is None:
            return None

        return self.target_type._api_representation(obj)


class ApiObjectMetaclass(type):
    @classmethod
    def _get_base_declared_properties(mcs, bases):
        properties = OrderedDict()

        for base in bases:
            if hasattr(base, "_declared_properties"):
                properties.update(base._declared_properties)

        return properties

    @classmethod
    def _get_declared_properties(mcs, attrs):
        declared_properties = OrderedDict()

        for attr_name in list(attrs.keys()):
            attr = attrs[attr_name]

            if isinstance(attr, Property):
                declared_properties[attr.name or attr_name] = attr
                del attrs[attr_name]

        return declared_properties

    def __new__(mcs, name, bases, attrs):
        all_declared_properties = OrderedDict()

        base_declared_properties = mcs._get_base_declared_properties(bases)
        declared_properties = mcs._get_declared_properties(attrs)

        all_declared_properties.update(base_declared_properties)
        all_declared_properties.update(declared_properties)

        attrs['_declared_properties'] = all_declared_properties

        return super().__new__(mcs, name, bases, attrs)


class ApiObject(metaclass=ApiObjectMetaclass):
    _declared_properties: Dict[str, Property] = None

    @classmethod
    def _patch(cls, data, old_value):
        if old_value is None:
            old_value = cls.__new__(cls)

        return old_value.patch(data)

    def patch(self, data):
        for field_name, data in data.items():
            property = self._declared_properties[field_name]

            old_value = getattr(self, property.property_name or field_name, None)

            setattr(self, property.property_name or field_name, property._patch(data, old_value))

        return self

    def is_valid(self):
        try:
            validate(self._api_representation(), self.schema())

            return True
        except ValidationError:
            return False

    def validation_errors(self):
        schema = self.schema()
        representation = self._api_representation()

        errors = [
            {
                "message": str(error.message),
                "path": "$." + ".".join([str(element) for element in error.absolute_path])
            }
            for error in validator_for(schema)(schema).iter_errors(representation)
        ]

        return errors

    @classmethod
    def ensure_definition(cls, definitions):
        definitions[cls.__name__] = None

        definition = {
            "type": "object",
            "properties": dict(
                (field_name, property.schema(definitions)) for field_name, property in cls._declared_properties.items()),
            "additionalProperties": False,
            "required": [field_name for field_name, property in cls._declared_properties.items() if property.required]
        }

        definitions[cls.__name__] = definition

        return definition

    @classmethod
    def schema(cls, definitions=None):
        append_definitions = False

        if definitions is None:
            definitions = dict()
            append_definitions = True

        if cls.__name__ in definitions:
            return {
                "$ref": "#/definitions/" + cls.__name__
            }

        cls.ensure_definition(definitions)

        if append_definitions:
            return {
                "definitions": definitions,
                "$ref": "#/definitions/" + cls.__name__
            }

        return {
            "$ref": "#/definitions/" + cls.__name__
        }

    def _api_representation(self):
        result = OrderedDict()

        for field_name, field_type in self._declared_properties.items():
            field_value = getattr(self, field_type.property_name or field_name, None)

            result[field_name] = field_type._api_representation(field_value)

        return result

    def __json__(self):
        return self._api_representation()


class PolymorphicApiObject(ApiObject):
    discriminator_name = "type"

    @classmethod
    def _patch(cls, data, old_value):
        if data is None:
            return None

        type = data[cls.discriminator_name]
        del data[cls.discriminator_name]

        discriminator_map = cls._discriminator_map()

        if type not in discriminator_map:
            raise Exception(f"Unknown type {type}")

        if type == old_value.__class__.__name__:
            return old_value.patch(data)

        old_value = discriminator_map[type].__new__(discriminator_map[type])

        return old_value.patch(data)

    @classmethod
    def _discriminator_map(cls):
        def recursive_discriminator_map(clazz):
            result = {}

            if not inspect.isabstract(clazz):
                result[clazz.__name__] = clazz

            for subclass in clazz.__subclasses__():
                result.update(recursive_discriminator_map(subclass))

            return result

        return recursive_discriminator_map(cls)

    @classmethod
    def _recursive_subclass_schema(cls, clazz, definitions):
        result = []

        for subclass in clazz.__subclasses__():
            if not inspect.isabstract(subclass):
                result.append(subclass.schema(definitions))

            result += cls._recursive_subclass_schema(subclass, definitions)

        return result

    @classmethod
    def ensure_definition(cls, definitions):
        definition = super().ensure_definition(definitions)

        # add discriminator property to properties
        definition["properties"][cls.discriminator_name] = {
            "const": cls.__name__
        }

        return definition

    @classmethod
    def schema(cls, definitions=None):
        append_definitions = False

        if definitions is None:
            definitions = dict()
            append_definitions = True

        if PolymorphicApiObject in cls.__bases__:
            schema = JsonSchema.any_of(*cls._recursive_subclass_schema(cls, definitions))

            if append_definitions:
                return {
                    "definitions": definitions,
                    **schema
                }
            else:
                return schema

        schema = super().schema(definitions)

        if append_definitions:
            return {
                "definitions": definitions,
                **schema
            }
        else:
            return schema

    def _api_representation(self):
        result = super()._api_representation()

        return {
            self.discriminator_name: self.__class__.__name__,
            **result
        }
