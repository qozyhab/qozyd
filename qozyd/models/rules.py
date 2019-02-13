from logdecorator import log_on_start
from persistent import Persistent
from persistent.list import PersistentList
import logging


logger = logging.getLogger(__name__)


class Rule(Persistent):
    __parent__ = None

    def __init__(self, name, qozy):
        self.name = name
        self.qozy = qozy
        self.triggers = PersistentList()
        self.conditions = PersistentList()
        self.actions = PersistentList()

    @property
    def __name__(self):
        return self.id

    @property
    def id(self):
        return ":".join(("rule", self.name))

    def add_trigger(self, trigger):
        trigger.add_rule(self)
        self.triggers.append(trigger)

    def delete_trigger(self, trigger):
        self.triggers.remove(trigger)
        trigger.delete_rule(self)

    def add_action(self, action):
        self.actions.append(action)
        action.__parent__ = self

    def delete_action(self, action):
        self.actions.remove(action)
        action.__parent__ = None

    def compile(self):
        raise NotImplementedError()

    @log_on_start(logging.INFO, "Executing rule {self.name:s}")
    def execute(self):
        raise NotImplementedError()

    def delete(self):
        for trigger in self.triggers:
            trigger.delete_rule(self)

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "triggers": list(self.triggers),
            "actions": list(self.actions),
        }


class ScriptRule(Rule):
    def __init__(self, name, qozy, script=""):
        super().__init__(name, qozy)

        self.script = script
        self._v_compilation = None

    def _ensure_compiled(self):
        if not getattr(self, "_v_compilation", None):
            self.compile()

    def compile(self):
        self._v_compilation = compile(self.script, "script_action.py", "exec")

    def execute(self):
        self._ensure_compiled()

        action_logger = logging.getLogger()

        items = {}
        for _, thing in self.qozy.things:
            for item in thing.items.values():
                items[item.id] = item

        rules = dict(self.qozy.rules)

        exec(self._v_compilation, {
            "apply": lambda item_id, value: items[item_id].thing.bridge.apply(items[item_id].thing,
                                                                              items[item_id].channel, value),
            "value": lambda item_id: items[item_id].value(),
            "call": lambda rule_id: rules[rule_id].execute(),
            "logger": action_logger
        })

    def __json__(self):
        return {
            **super().__json__(),
            **{
                "script": self.script,
            }
        }
