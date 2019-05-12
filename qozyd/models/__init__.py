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

    @property
    def id(self):
        return "system"

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

    def thing(self, thing_id):
        for bridge in self.bridges.values():
            for thing in bridge.things.values():
                if thing.id == thing_id:
                    return thing

        return None

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

        raise KeyError

    def __json__(self):
        return {
            "bridges": dict(self.bridges),
            "things": dict(self.things),
            "rules": dict(self.rules),
            "notifications": list(self.notifications),
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
