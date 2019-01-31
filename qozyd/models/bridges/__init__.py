import threading
from builtins import NotImplementedError

import jsonschema
from persistent import Persistent
from persistent.mapping import PersistentMapping

from qozyd.utils.events import new_thing_found


class Bridge(Persistent):
    VENDOR_PREFIX = None
    SETTINGS_SCHEMA = {}

    _v_stop_event = threading.Event()

    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.things = PersistentMapping()
        self.settings = PersistentMapping()

        self._v_stop_event = threading.Event()

    @property
    def id(self):
        return ":".join(("bridge", self.VENDOR_PREFIX, self.instance_id))

    @property
    def active(self):
        return self.settings != {}

    def start(self, connection):
        raise NotImplementedError()

    @property
    def stopped(self):
        return self._v_stop_event.is_set()

    def stop(self):
        self._v_stop_event.set()

    def set_settings(self, settings):
        try:
            jsonschema.validate(settings, self.SETTINGS_SCHEMA)
            self.settings.clear()
            self.settings.update(settings)
            self._p_changed = True

            return True
        except jsonschema.ValidationError:
            raise
            
    def add_thing(self, thing):
        if thing.id in self.things:
            self.update_state(self.things[thing.id])
            return

        # call event
        new_thing_found(thing)

        thing.bridge = self

        self.things[thing.id] = thing

    def remove_thing(self, thing):
        del self.things[thing.id]
        thing.bridge = None

    def scan(self):
        raise NotImplementedError

    def is_online(self, local_id):
        raise NotImplementedError

    def apply(self, local_id, name, value):
        raise NotImplementedError

    def __getitem__(self, item):
        return self.things[item]

    def __json__(self):
        return {
            "id": self.id,
            "active": self.active,
            "vendorPrefix": self.VENDOR_PREFIX,
            "instanceId": self.instance_id,
            "settingsSchema": self.SETTINGS_SCHEMA,
            "settings": dict(self.settings),
            "things": dict(self.things),
        }
