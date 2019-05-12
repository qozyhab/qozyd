import asyncio
import threading
from asyncio import AbstractEventLoop, CancelledError

import time
import logging
from logdecorator import log_on_start

from qozyd.context import ContextExecutable, AsyncContextExecutable
from qozyd.models import Qozy
from qozyd.models.bridges import Bridge
from qozyd.models.channels import Channel
from qozyd.models.things import Thing
from qozyd.plugins.bridge import BridgePlugin
from transaction import TransactionManager
from typing import Dict, Awaitable

logger = logging.getLogger(__name__)


class BridgeRunner(threading.Thread):
    def __init__(self, bridge: Bridge, connection_factory):
        super().__init__()

        self.bridge = bridge
        self.bridge_plugin: BridgePlugin = bridge.plugin_class(bridge)
        self.stop_event = threading.Event()
        self.connection_factory = connection_factory
        self.event_loop: AbstractEventLoop = None

    def stop(self):
        self.stop_event.set()
        self.bridge_plugin.stop()
        self.event_loop.stop()

        # stop all pending tasks
        for task in asyncio.all_tasks(self.event_loop):
            task.cancel()

    @property
    def stopped(self):
        return self.stop_event.is_set()

    async def _run_async(self):
        connection = self.connection_factory()

        while not self.stopped:
            try:
                await self.bridge_plugin.start(connection)
            except Exception as e:
                if not self.stopped:
                    logger.error(
                        f"Bridge \"{self.bridge.id}\" stopped unexpected, restarting in 1 second, reason: {str(e)}")
                    logger.exception(e)
                    time.sleep(1)

    def run(self):
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        try:
            self.event_loop.run_until_complete(self._run_async())
        except CancelledError:
            pass

        self.event_loop.close()


class BridgeManager(AsyncContextExecutable):
    def __init__(self, app_root: Qozy, transaction_manager: TransactionManager, connection_factory):
        super().__init__()

        self.root = app_root
        self.transaction_manager = transaction_manager
        self.connection_factory = connection_factory

        self.running_bridges: Dict[str, BridgeRunner] = {}
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

        for bridge_runner in self.running_bridges.values():
            bridge_runner.stop()

    @property
    def stopped(self):
        return self.stop_event.is_set()

    @log_on_start(logging.INFO, "Starting Bridge \"{bridge.id:s}\"")
    def start_bridge(self, bridge):
        self.running_bridges[bridge.id] = BridgeRunner(bridge, self.connection_factory)
        self.running_bridges[bridge.id].start()

    @log_on_start(logging.INFO, "Stopping Bridge \"{bridge:s}\"")
    def stop_bridge(self, bridge):
        self.running_bridges[bridge.id].stop()
        self.running_bridges[bridge.id].join()

        del self.running_bridges[bridge.id]

    @property
    def active_bridges(self):
        return dict((bridge_id, bridge) for bridge_id, bridge in self.root.bridges.items() if bridge.active and bridge.plugin_class(bridge).active)

    @log_on_start(logging.INFO, "Scanning for new things")
    async def scan(self):
        new_things = 0

        for bridge_runner in self.running_bridges.values():
            with self.transaction_manager:
                async for thing in bridge_runner.bridge_plugin.scan():
                    if bridge_runner.bridge.add_thing(thing):
                        logger.info(f"New thing found {thing.id} via bridge {bridge_runner.bridge.id}")
                        new_things += 1

        return new_things

    @log_on_start(logging.INFO, "Find things")
    async def find(self):
        for bridge_runner in self.running_bridges.values():
            bridge_plugin = bridge_runner.bridge_plugin
            await bridge_plugin.find()

    def is_online(self, thing: Thing):
        if thing.bridge.id not in self.running_bridges:
            return False

        bridge_runner = self.running_bridges[thing.bridge.id]

        return bridge_runner.bridge_plugin.is_online(thing)

    async def apply(self, thing: Thing, channel: Channel, value) -> Awaitable[bool]:
        if channel.sensor:
            raise Exception(f"Channel {channel.name} is in sensor mode")

        bridge_runner = self.running_bridges[thing.bridge.id]

        return await bridge_runner.bridge_plugin.apply(thing, channel, value)

    def is_active(self, bridge: Bridge):
        return bridge in self.active_bridges.values()

    async def start(self):
        while not self.stopped:
            # run all active bridges
            available_bridges = self.active_bridges

            # stop inactive/inavailable but still running bridges
            for bridge_runner in self.running_bridges.values():
                if not self.is_active(bridge_runner.bridge):
                    self.stop_bridge(bridge_runner.bridge)

            # start non running active bridges
            for bridge_id, bridge in available_bridges.items():
                if bridge_id not in self.running_bridges:
                    self.start_bridge(bridge)

            await asyncio.sleep(1)
