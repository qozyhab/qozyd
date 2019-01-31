from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

from datetime import datetime


class Qozy(Persistent):
    def __init__(self):
        self.bridges = PersistentMapping()
        self.rules = PersistentMapping()
        self.notifications = PersistentList()
        self.plugins = PersistentMapping()
        self._triggers = {}

        self._add_trigger(Trigger("started"))

    @property
    def id(self):
        return "system"

    def _add_trigger(self, trigger):
        self._triggers[trigger.event_name] = trigger

    def trigger(self, event_name):
        return self._triggers[event_name]

    def add_bridge(self, bridge):
        self.bridges[bridge.id] = bridge

    def delete_bridge(self, bridge):
        del self.bridges[bridge.id]

    def add_rule(self, rule):
        self.rules[rule.id] = rule

    def delete_rule(self, rule):
        del self.rules[rule.id]

    @property
    def things(self):
        for bridge in self.bridges.values():
            for thing in bridge.things.values():
                yield thing.id, thing

    @property
    def items(self):
        for bridge in self.bridges.values():
            for thing in bridge.things.values():
                for item in thing.items.values():
                    yield item.id, item

    @property
    def triggers(self):
        for trigger in self._triggers.values():
            yield trigger.id, trigger

        for _, thing in self.things:
            for trigger in thing.triggers.values():
                yield trigger.id, trigger

            for item in thing.items.values():
                for trigger in item.triggers.values():
                    yield trigger.id, trigger

    def add_notification(self, notification):
        self.notifications.insert(0, notification)

    def delete_notification(self, notification):
        if notification.dismissable:
            self.notifications.remove(notification)

    def get_or_create_plugin_store(self, name):
        if name not in self.plugins:
            self.plugins[name] = PersistentMapping()

        return self.plugins[name]

    def __getitem__(self, item):
        if item.startswith("rule:"):
            return self.rules[item]
        elif item.startswith("bridge:"):
            return self.bridges[item]
        elif item.startswith("thing:"):
            return dict(self.things)[item]
        elif item.startswith("item:"):
            return dict(self.items)[item]

        raise KeyError

    def __json__(self):
        return {
            "bridges": dict(self.bridges),
            "things": dict(self.things),
            "rules": dict(self.rules),
            "triggers": dict(self.triggers),
            "notifications": list(self.notifications),
        }


class Trigger(Persistent):
    __parent__ = None

    def __init__(self, event_name):
        self.event_name = event_name
        self.rules = PersistentList()

    @property
    def id(self):
        return ":".join(("trigger", self.__parent__.id, self.event_name))

    def add_rule(self, rule):
        self.rules.append(rule)

    def delete_rule(self, rule):
        self.rules.remove(rule)

    @property
    def __name__(self):
        return self.id

    def fire(self):
        for rule in self.rules:
            rule.execute()

    def __json__(self):
        return {
            "id": self.id,
            "eventName": self.event_name,
            "parent": self.__parent__.id
        }


class HistoricalValue(Persistent):
    def __init__(self, value):
        self.value = value
        self.date = datetime.now()

    def __json__(self):
        return {
            "value": self.value,
            "date": self.date
        }
