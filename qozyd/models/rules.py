from persistent import Persistent
from persistent.list import PersistentList
import itertools
import logging


class Action(Persistent):
    def validate(self):
        raise NotImplementedError()

    def execute(self, qozy):
        raise NotImplementedError()

    def __json__(self):
        return {
            "_type": self.__class__.__name__,
        }


class ScriptAction(Action):
    def __init__(self, script=""):
        self.script = script
        self._v_compilation = None

    def _compile(self):
        return compile(self.script, "script_action.py", "exec")
    
    def _ensure_compiled(self):
        if not getattr(self, "_v_compilation", None):
            setattr(self, "_v_compilation", self._compile())

    def validate(self):
        self._compile()

    def execute(self, qozy):
        self._ensure_compiled()

        action_logger = logging.getLogger()

        items = {}
        for _, thing in qozy.things:
            for item in thing.items.values():
                items[item.id] = item

        rules = dict(qozy.rules)

        exec(self._v_compilation, {
            "apply": lambda item_id, value: items[item_id].thing.bridge.apply(items[item_id].thing, items[item_id].channel, value),
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

    def execute(self):
        # ugly, for debug purposes only
        # eval(self.script)
        print("Executing rule %s!" % self.name)

        for action in self.actions:
            action.execute(self.qozy)

    def delete(self):
        for trigger in self.triggers:
            trigger.delete_rule(self)

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "triggers": list(self.triggers),
            "actions": list(self.actions),
            # "@actions": {
            #     "delete": {
            #         "method": "DELETE",
            #         "url": request.resource_path(self),
            #         "payload": False,
            #     },
            #     "addTrigger": {
            #         "method": "POST",
            #         "url": request.resource_path(self, "add-trigger"),
            #         "payload": True,
            #         "payloadSchema": {
            #             "type": "string"
            #         }
            #     },
            #     "deleteTrigger": {
            #         "method": "DELETE",
            #         "url": request.resource_path(self, "delete-trigger"),
            #         "payload": True,
            #         "payloadSchema": {
            #             "type": "string"
            #         }
            #     },
            #     "addAction": {
            #         "method": "POST",
            #         "url": request.resource_path(self, "add-action"),
            #         "payload": True,
            #         "payloadSchema": {
            #             "type": "object",
            #             "properties": {
            #                 "type": {
            #                     "type": "string",
            #                     "enum": ["ScriptAction"],
            #                 },
            #                 "payload": {
            #                     "type": "object",
            #                     "properties": {
            #                         "script": {
            #                             "type": "string"
            #                         }
            #                     }
            #                 }
            #             }
            #         }
            #     },
            #     "deleteAction": {
            #         "method": "DELETE",
            #         "url": request.resource_path(self, "delete-action"),
            #         "payload": True,
            #         "payloadSchema": {
            #             "type": "number"
            #         }
            #     }
            # }
        }
