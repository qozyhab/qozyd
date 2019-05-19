import threading
from builtins import NotImplementedError

import jsonschema
from persistent import Persistent
from persistent.mapping import PersistentMapping

from qozyd.utils.events import new_thing_found


class Bridge(Persistent):
    active = True

    def __init__(self, instance_id, plugin_class):
        self.instance_id = instance_id
        self.things = PersistentMapping()
        self.settings = PersistentMapping()
        self.plugin_class = plugin_class
        self.active = True

    @property
    def id(self):
        return ":".join(("bridge", self.plugin_class.VENDOR_PREFIX, self.instance_id))

    def set_settings(self, settings):
        try:
            jsonschema.validate(settings, self.plugin_class.SETTINGS_SCHEMA)
            self.settings.clear()
            self.settings.update(settings)
            self._p_changed = True

            return True
        except jsonschema.ValidationError:
            raise
            
    async def add_thing(self, thing):
        if thing.id in self.things:
            return False

        # call event
        await new_thing_found(thing)

        thing.bridge = self

        self.things[thing.id] = thing

        return True

    def remove_thing(self, thing):
        del self.things[thing.id]
        thing.bridge = None

    def __getitem__(self, item):
        return self.things[item]

    def __json__(self):
        return {
            "id": self.id,
            "vendorPrefix": self.plugin_class.VENDOR_PREFIX,
            "instanceId": self.instance_id,
            "settingsSchema": self.plugin_class.SETTINGS_SCHEMA,
            "settings": dict(self.settings),
            "active": self.active,
            "things": dict(self.things),
        }
