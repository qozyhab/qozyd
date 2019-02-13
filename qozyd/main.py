import os
import argparse
import logging

from ZODB import DB
import transaction

from functools import partial

from qozyd.context import HttpContext
from qozyd.http_server import HttpServer
from qozyd.models import Qozy
from qozyd.services.router import QozyRouter
from qozyd.services.service_container import Reference, Service, Instance


logger = logging.getLogger(__name__)


def create_db(database_path):
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    db = DB(database_path)

    return db


def create_connection(db, transaction_manager=None):
    if transaction_manager is None:
        transaction_manager = transaction.TransactionManager()

    connection = db.open(transaction_manager)
    connection.sync()

    # ensure "app_root" exists
    if "app_root" not in connection.root():
        with transaction_manager:
            connection.root()["app_root"] = Qozy()

    return connection


def get_app_root(connection):
    return connection.root()["app_root"]


def main():
    parser = argparse.ArgumentParser(description="qozyd daemon")
    parser.add_argument("-d", "--debug", dest="debug", action="store_true")
    parser.add_argument("--host", dest="host", type=str, default="localhost")
    parser.add_argument("--port", dest="port", type=int, default=9876)
    parser.add_argument("--database", dest="database", type=str, default=os.path.expanduser("~/.qozy/Data.fs"))

    options = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if options.debug else logging.INFO,
                        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")

    db = create_db(options.database)

    services = (
        # Database
        Instance(db, name="db", ),
        Service("transaction.TransactionManager", name="transaction_manager"),
        Service(create_connection, name="connection",
                inject=(Reference("db"), Reference("transaction_manager"),)),
        Service(get_app_root, name="app_root", inject=(Reference("connection"),)),
        Instance(partial(create_connection, db), name="connection_factory"),

        # Logic Services
        Service("qozyd.services.notification_manager.NotificationManager", name="notification_manager",
                inject=(Reference("db"),)),
        Service("qozyd.services.plugin_manager.PluginManager", name="plugin_manager", inject=(
        Reference("app_root"), Reference("transaction_manager"), Reference("service_container"),
        Reference("context"),)),
        Service("qozyd.services.bridge_manager.BridgeManager", name="bridge_manager",
                inject=(Reference("app_root"), Reference("transaction_manager"), Reference("connection_factory"),)),

        # Controllers
        Service("qozyd.controller.StaticFileController", name="controller.static_file"),
        Service("qozyd.controller.QozyController", name="controller.qozy"),
        Service("qozyd.controller.BridgeController", name="controller.bridge",
                inject=(Reference("app_root"), Reference("plugin_manager"), Reference("transaction_manager"),)),
        Service("qozyd.controller.ThingController", name="controller.thing",
                inject=(Reference("app_root"), Reference("transaction_manager"),)),
        Service("qozyd.controller.ChannelController", name="controller.channel",
                inject=(Reference("app_root"), Reference("transaction_manager"),)),
        Service("qozyd.controller.RuleController", name="controller.rule",
                inject=(Reference("app_root"), Reference("transaction_manager"),)),
        Service("qozyd.controller.TriggerController", name="controller.trigger", inject=(Reference("app_root"),)),
        Service("qozyd.controller.NotificationController", name="controller.notification",
                inject=(Reference("app_root"),)),
    )

    http_context = HttpContext(services, router=QozyRouter())
    http_context.start()

    HttpServer(http_context, options.host, options.port).start()

    http_context.stop()


if __name__ == "__main__":
    main()
