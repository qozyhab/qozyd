from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import TreeSet

from qozyd.models.bridges import Bridge
from qozyd.models import Trigger
from qozyd.models.channels import Channel


class Thing(Persistent):
    def __init__(self, bridge: Bridge, local_id: str):
        self.bridge = bridge
        self.local_id = local_id
        self.channels = PersistentMapping()
        self.name = None
        self.triggers = PersistentMapping()
        self.tags = TreeSet()

        self._add_trigger(Trigger("online"))
        self._add_trigger(Trigger("offline"))

    @property
    def id(self) -> str:
        return ":".join(("thing", self.bridge.id, self.local_id))

    def _add_trigger(self, trigger: Trigger):
        self.triggers[trigger.event_name] = trigger

    def trigger(self, event_name: str) -> Trigger:
        return self.triggers[event_name]

    def add_channel(self, channel: Channel):
        channel.thing = self
        self.channels[channel.name] = channel

    def channel(self, channel_name: str) -> Channel:
        return self.channels[channel_name]

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    def is_online(self):
        return self.bridge.is_online(self)

    def __getitem__(self, channel_name: str) -> Channel:
        return self.channel(channel_name)

    def __json__(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "bridge_id": self.bridge.id,
            "channels": dict(self.channels),
            "tags": set(self.tags),
        }
