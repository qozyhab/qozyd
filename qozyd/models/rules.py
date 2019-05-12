import asyncio

from persistent import Persistent
from enum import Enum
import logging

from qozyd.models.channels import SwitchChannel, NumberChannel, StringChannel, ColorChannel
from qozyd.utils.api import Field, Relation, Array, Const, PolymorphicApiObject
from qozyd.utils.color import RGB, HSL, HSV

logger = logging.getLogger(__name__)


class CompiledRule():
    def __init__(self, activator, deactivator, executable):
        self.activator = activator
        self.deactivator = deactivator
        self.exetuable = executable

    async def activate(self):
        await self.activator()

    async def execute(self):
        await self.exetuable()

    async def deactivate(self):
        await self.deactivator()


class Rule(Persistent, PolymorphicApiObject):
    __parent__ = None

    id = Field("string")
    name = Field("string", required=False, nullable=True)

    def __init__(self, id, qozy):
        self.id = id
        self.name = None
        self.qozy = qozy

    async def compile(self, bridge_manager):
        raise NotImplementedError()


class Type(Enum):
    BOOL = 1
    NUMERIC = 2
    STRING = 3
    COLOR = 4


class Expression(PolymorphicApiObject):
    # def type(self, qozy):
    #     raise NotImplementedError()

    def evaluate(self, qozy):
        raise NotImplementedError()

    def nodes_by_type(self, type):
        if isinstance(self, type):
            return [self]

        return []


class ExpressionContainer(Expression):
    inputs = Array(Relation(Expression))

    def nodes_by_type(self, type):
        result = super().nodes_by_type(type)

        for input in self.inputs:
            result += input.nodes_by_type(type)

        return result


class Literal(Expression):
    group = Const("literal")


class ConstValue(Literal):
    value = Field(["string", "number", "boolean"])

    def __init__(self, value):
        self.value = value

    # def type(self, qozy):
    #     if isinstance(self.value, str):
    #         return Type.STRING
    #     elif isinstance(self.value, bool):
    #         return Type.BOOL
    #     elif isinstance(self.value, (int, float)):
    #         return Type.NUMERIC
    #
    #     raise Exception(f"Unknown ConstValue type {type(self.value)} ({str(self.value)})")

    def evaluate(self, qozy):
        return self.value

    # def __json__(self):
    #     return {
    #         "type": self.__class__.__name__,
    #         "class": "literal",
    #         "value": self.value,
    #     }


class ChannelValue(Literal):
    thing_id = Field("string")
    channel_name = Field("string")

    def __init__(self, thing_id, channel_name):
        self.thing_id = thing_id
        self.channel_name = channel_name

    # def type(self, qozy):
    #     channel = qozy.thing(self.thing_id).channel(self.channel_name)
    #
    #     if isinstance(channel, SwitchChannel):
    #         return Type.BOOL
    #     elif isinstance(channel, NumberChannel):
    #         return Type.NUMERIC
    #     elif isinstance(channel, StringChannel):
    #         return Type.STRING
    #     elif isinstance(channel, ColorChannel):
    #         return Type.COLOR
    #
    #     raise Exception(f"Unknown Channel Type {str(channel.__class__.__name__)}")

    def evaluate(self, qozy):
        return qozy.thing(self.thing_id).channel(self.channel_name).value

    # def __json__(self):
    #     return {
    #         "type": self.__class__.__name__,
    #         "class": "literal",
    #         "thing_id": self.thing_id,
    #         "channel_name": self.channel_name,
    #     }


class Logical(ExpressionContainer):
    group = Const("logical")

    def __init__(self, inputs):
        self.inputs = inputs


class And(Logical):
    # def type(self, qozy):
    #     return Type.BOOL

    def evaluate(self, qozy):
        if all(expression.evaluate(qozy) for expression in self.inputs):
            return True

        return False

    # def __json__(self):
    #     return {
    #         "type": self.__class__.__name__,
    #         "class": "logical",
    #         "inputs": list(self.expressions)
    #     }


class Or(Logical):
    # def type(self, qozy):
    #     return Type.BOOL

    def evaluate(self, qozy):
        if any(expression.evaluate(qozy) for expression in self.inputs):
            return True

        return False

    # def __json__(self):
    #     return {
    #         "type": self.__class__.__name__,
    #         "class": "logical",
    #         "inputs": list(self.expressions)
    #     }


class BinaryOperation(ExpressionContainer):
    group = Const("binary")
    inputs = Array(Relation(Expression, nullable=True), min_items=2, max_items=2)
    # left_expression = Relation(Expression)
    # right_expression = Relation(Expression)

    def __init__(self, left_expression=None, right_expression=None):
        self.inputs = []
        self.inputs.append(left_expression)
        self.inputs.append(right_expression)

    @property
    def left_expression(self):
        return self.inputs[0]

    @property
    def right_expression(self):
        return self.inputs[1]

    # def __json__(self):
    #     return {
    #         "type": self.__class__.__name__,
    #         "class": "binary",
    #         "left_expression": self.left_expression,
    #         "right_expression": self.right_expression,
    #     }


class Equals(BinaryOperation):
    # def type(self, qozy):
    #     return Type.BOOL

    def evaluate(self, qozy):
        return self.left_expression.evaluate(qozy) == self.right_expression.evaluate(qozy)


class NotEquals(BinaryOperation):
    def evaluate(self, qozy):
        return self.left_expression.evaluate(qozy) != self.right_expression.evaluate(qozy)


class GreaterThan(BinaryOperation):
    # def type(self, qozy):
    #     return Type.BOOL

    def evaluate(self, qozy):
        return self.left_expression.evaluate(qozy) > self.right_expression.evaluate(qozy)


class GreaterThanOrEquals(BinaryOperation):
    # def type(self, qozy):
    #     return Type.BOOL

    def evaluate(self, qozy):
        return self.left_expression.evaluate(qozy) >= self.right_expression.evaluate(qozy)


class LowerThan(BinaryOperation):
    # def type(self, qozy):
    #     return Type.BOOL

    def evaluate(self, qozy):
        return self.left_expression.evaluate(qozy) < self.right_expression.evaluate(qozy)


class LowerThanOrEquals(BinaryOperation):
    # def type(self, qozy):
    #     return Type.BOOL

    def evaluate(self, qozy):
        return self.left_expression.evaluate(qozy) <= self.right_expression.evaluate(qozy)


class ScriptRule(Rule):
    condition = Relation(Expression, required=False, nullable=True)
    script = Field("string")

    def __init__(self, id, qozy, condition=None, script=""):
        super().__init__(id, qozy)

        self.condition = condition
        self.script = script

    async def compile(self, bridge_manager):
        compilation = compile(self.script, "script_action.py", "exec")
        attached_channels = [(channel_value_expression.thing_id, channel_value_expression.channel_name) for channel_value_expression in self.condition.nodes_by_type(ChannelValue)]

        async def execute():
            action_logger = logging.getLogger(name=f"Rule: {self.name or self.id}")

            rules = dict(self.qozy.rules)

            def set(thing_id, channel, value):
                thing = self.qozy[thing_id]
                channel = thing.channel(channel)

                asyncio.ensure_future(bridge_manager.apply(thing, channel, value))

            exec(compilation, {
                "set": set,
                "value": lambda thing_id, channel: self.qozy[thing_id].channel(channel).value,
                "call": lambda rule_id: rules[rule_id].execute(bridge_manager),
                "logger": action_logger,
                "RGB": RGB,
                "HSV": HSV,
                "HSL": HSL,
            })

            return True

        async def callback(*args, **kwargs):
            if self.condition.evaluate(self.qozy):
                await execute()

        async def activate():
            # await callback()

            for thing_id, channel_name in attached_channels:
                self.qozy[thing_id].channel(channel_name).on_change.append(callback)

        async def deactivate():
            for thing_id, channel_name in attached_channels:
                self.qozy[thing_id].channel(channel_name).on_change.remove(callback)

        return CompiledRule(activate, deactivate, execute)
