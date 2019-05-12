from persistent import Persistent
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import TreeSet

from qozyd.models.bridges import Bridge
from qozyd.models.channels import Channel


class Thing(Persistent):
    def __init__(self, bridge: Bridge, local_id: str):
        self.bridge = bridge
        self.local_id = local_id
        self.channels = PersistentMapping()
        self.name = None
        self.tags = TreeSet()

    @property
    def id(self) -> str:
        return ":".join(("thing", self.bridge.id, self.local_id))

    def add_channel(self, channel: Channel):
        channel.thing = self
        self.channels[channel.name] = channel

    def channel(self, channel_name: str) -> Channel:
        return self.channels[channel_name]

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

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
