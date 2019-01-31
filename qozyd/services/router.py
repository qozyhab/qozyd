from qozyd.http import Router, Route
import re

routes = [
    Route(re.compile(r'^/$'), ("controller.qozy", "info"), method="GET"),

    Route(re.compile(r'^/bridges$'),
          ("controller.bridge", "bridges"), method="GET"),
    Route(re.compile(r'^/bridges/types$'),
          ("controller.bridge", "types"), method="GET"),
    Route(re.compile(r'^/bridges$'),
          ("controller.bridge", "add"), method="POST"),
    Route(re.compile(
        r'^/bridges/(?P<bridge_id>[^/]+)$'), ("controller.bridge", "bridge"), method="GET"),
    Route(re.compile(r'^/bridges/(?P<bridge_id>[^/]+)$'),
          ("controller.bridge", "remove"), method="DELETE"),
    Route(re.compile(r'^/bridges/(?P<bridge_id>[^/]+)/things$'),
          ("controller.bridge", "things"), method="GET"),
    Route(re.compile(r'^/bridges/(?P<bridge_id>[^/]+)/settings$'),
          ("controller.bridge", "settings_set"), method="PUT"),

    Route(re.compile(r'^/things$'), ("controller.thing", "things"), method="GET"),
    Route(re.compile(r'^/things/scan$'), ("controller.thing", "scan"), method="GET"),
    Route(re.compile(r'^/things/tags$'),
          ("controller.thing", "tags"), method="GET"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)$'), ("controller.thing", "thing"), method="GET"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/items$'), ("controller.thing", "items"), method="GET"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/items/(?P<item_id>[^/]+)$'), ("controller.thing", "item"), method="GET"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/name$'), ("controller.thing", "set_name"), method="PUT"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/tags$'), ("controller.thing", "tag_add"), method="POST"),
    Route(re.compile(r'^/things/(?P<thing_id>[^/]+)/tags$'),
          ("controller.thing", "tag_remove"), method="DELETE"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/online$'), ("controller.thing", "online"), method="GET"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)$'), ("controller.thing", "remove"), method="DELETE"),

    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/set/(?P<channel_name>[^/]+)$'), ("controller.channel", "set"), method="PUT"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/set/(?P<channel_name>[^/]+)/on$'), ("controller.channel", "on"), method="PUT"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/set/(?P<channel_name>[^/]+)/off$'), ("controller.channel", "off"), method="PUT"),
    Route(re.compile(
        r'^/things/(?P<thing_id>[^/]+)/set/(?P<channel_name>[^/]+)/toggle$'), ("controller.channel", "toggle"), method="PUT"),

    # Route(re.compile(
    #     r'^/items$'), ("controller.item", "items"), method="GET"),
    # Route(re.compile(
    #     r'^/items/(?P<item_id>[^/]+)$'), ("controller.item", "item"), method="GET"),
    # Route(re.compile(
    #     r'^/items/(?P<item_id>[^/]+)$'), ("controller.item", "apply"), method="PUT"),

    Route(re.compile(r'^/rules$'), ("controller.rule", "rules"), method="GET"),
    Route(re.compile(
        r'^/rules/(?P<rule_id>[^/]+)$'), ("controller.rule", "rule"), method="GET"),
    Route(re.compile(r'^/rules$'), ("controller.rule", "add"), method="POST"),
    Route(re.compile(r'^/rules/(?P<rule_id>[^/]+)/trigger$'),
          ("controller.rule", "add_trigger"), method="POST"),

    Route(re.compile(r'^/triggers$'),
          ("controller.trigger", "triggers"), method="GET"),
    Route(re.compile(
        r'^/triggers/(?P<trigger_id>[^/]+)$'), ("controller.trigger", "trigger"), method="GET"),

    Route(re.compile(r'^/notifications$'),
          ("controller.notification", "notificiations"), method="GET"),
    Route(re.compile(r'^/notifications/(?P<index>[1-9][0-9]*)$'),
          ("controller.notification", "remove"), method="DELETE"),

    Route(re.compile(r'^/plugins$'),
          ("controller.plugin", "plugins"), method="GET"),
    Route(re.compile(r'^/plugins/available$'),
          ("controller.plugin", "available"), method="GET"),
    Route(re.compile(r'^/plugins$'),
          ("controller.plugin", "install"), method="POST"),
    Route(re.compile(r'^/plugins$'),
          ("controller.plugin", "remove"), method="DELETE"),
    Route(r"^/plugins/(?P<plugin>[^/]+)", ("controller.plugin", "plugin")),
]


class QozyRouter(Router):
    def __init__(self):
        super().__init__(routes)
