import threading
import time
import logging
from logdecorator import log_on_start


logger = logging.getLogger(__name__)


class BridgeRunner(threading.Thread):
    def __init__(self, bridge, connection_factory):
        super().__init__()

        self.bridge = bridge
        self.stop_event = threading.Event()
        self.connection_factory = connection_factory

    def stop(self):
        self.stop_event.set()
        self.bridge.stop()

    @property
    def stopped(self):
        return self.stop_event.is_set()

    def run(self):
        connection = self.connection_factory()

        while not self.stopped:
            try:
                self.bridge.start(connection)
            except Exception as e:
                if not self.stopped:
                    logger.error("Bridge \"{bridge.id:s}\" stopped unexpected, restarting in 1 second, reason: {exception:s}".format(bridge=self.bridge, exception=str(e)))
                    logger.exception(e)
                    time.sleep(1)


class BridgeManager(threading.Thread):
    def __init__(self, app_root, transaction_manager, connection_factory):
        super().__init__()

        self.root = app_root
        self.transaction_manager = transaction_manager
        self.connection_factory = connection_factory

        self.running_bridges = {}
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
        return dict((bridge_id, bridge) for bridge_id, bridge in self.root.bridges.items() if bridge.active)

    def run(self):
        while not self.stopped:
            # run all active bridges
            available_bridges = self.active_bridges

            # stop inactive/inavailable but still running bridges
            for bridge_id, bridge in list(self.running_bridges.items()):
                if bridge_id not in available_bridges:
                    self.stop_bridge(bridge)

            # start non running active bridges
            for bridge_id, bridge in available_bridges.items():
                if bridge_id not in self.running_bridges:
                    self.start_bridge(bridge)                    
            
            time.sleep(1)
