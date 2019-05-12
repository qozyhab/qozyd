import threading
from ZODB.Connection import Connection
from qozyd.models.bridges import Bridge
from qozyd.models.channels import Channel
from qozyd.models.things import Thing
from typing import Iterable, Dict, Awaitable


class BridgePlugin():
    VENDOR_PREFIX = None
    SETTINGS_SCHEMA = {}

    def __init__(self, bridge: Bridge):
        self.bridge = bridge
        self.stop_event = threading.Event()

    async def start(self, connection: Connection):
        raise NotImplementedError()

    @property
    def settings(self) -> Dict:
        return self.bridge.settings

    @property
    def active(self) -> bool:
        return self.settings is not None and self.settings != {}

    @property
    def things(self) -> Dict[str, Thing]:
        return self.bridge.things

    @property
    def stopped(self) -> bool:
        return self.stop_event.is_set()

    def stop(self):
        self.stop_event.set()

    async def find(self):
        pass

    async def scan(self) -> Iterable[Thing]:
        raise NotImplementedError

    def is_online(self, local_id: str) -> bool:
        raise NotImplementedError

    async def apply(self, thing: Thing, channel: Channel, value) -> Awaitable[bool]:
        raise NotImplementedError
