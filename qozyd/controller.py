import logging
import os
import uuid

from logdecorator import log_on_start, log_on_end

from qozyd.http.decorator import json_response
from qozyd.http.exceptions import NotFoundException
from qozyd.http.response import FileResponse
from qozyd.models.rules import Rule

from qozyd import VERSION


logger = logging.getLogger(__name__)


class StaticFileController():
    def handle(self, request, path, base_path=None, directory_index=None):
        file_path = os.path.join(base_path or "", path)

        if os.path.isdir(file_path) and directory_index is not None:
            if isinstance(directory_index, str):
                file_path = os.path.join(file_path, directory_index)
            else:
                # try all directory_index files
                for directory_index_file in directory_index:
                    test_file_path = os.path.join(file_path, directory_index_file)

                    if os.path.isfile(test_file_path):
                        file_path = test_file_path
                        break
                else:
                    raise NotFoundException

        if not os.path.isfile(file_path):
            raise NotFoundException

        return FileResponse(file_path)


class QozyController():
    @json_response
    def info(self, request):
        return {
            "version": VERSION
        }


class BridgeController():
    def __init__(self, app_root, plugin_manager, transaction_manager):
        self.root = app_root
        self.plugin_manager = plugin_manager
        self.transaction_manager = transaction_manager
    
    @json_response
    def bridges(self, request):
        expand = request.get.get_bool("expand", False)

        if expand:
            return dict(self.root.bridges)
        
        return list(self.root.bridges.keys())

    @json_response
    def bridge(self, request, bridge_id):
        return self.root.bridges[bridge_id]

    @json_response
    def remove(self, request, bridge_id):
        with self.transaction_manager:
            self.root.delete_bridge(self.root.bridges[bridge_id])

        return True

    @json_response
    def things(self, request, bridge_id):
        return dict(self.root.bridges[bridge_id].things)

    @json_response
    def types(self, request):
        return list(self.plugin_manager.bridge_plugins().keys())

    @json_response
    def add(self, request):
        bridge_type = request.request_json

        bridge_class = self.plugin_manager.bridge_class(bridge_type)
        bridge = bridge_class(str(uuid.uuid4()))

        with self.transaction_manager:
            logging.info("Adding bridge of type {} with id {}".format(bridge_type, bridge.id))
            self.root.add_bridge(bridge)

        return bridge.id

    @json_response
    def settings_set(self, request, bridge_id):
        settings = request.request_json

        with self.transaction_manager:
            result = self.root.bridges[bridge_id].set_settings(settings)

        return result


class ThingController():
    def __init__(self, app_root, transaction_manager):
        self.root = app_root
        self.transaction_manager = transaction_manager
    
    @json_response
    def things(self, request):
        things = dict(self.root.things)

        expand = request.get.get_bool("expand", False)
        filter_tags = request.get.get("tag", None)

        if filter_tags:
            things = {id: thing for id, thing in things.items() if any(tag in filter_tags for tag in thing.tags)}

        if expand:
            return things
        
        return list(things.keys())
    
    @json_response
    def tags(self, request):
        things = dict(self.root.things)

        tags = set()

        for thing in things.values():
            tags = tags.union(thing.tags)

        return tags

    @json_response
    def thing(self, request, thing_id):
        return self.root[thing_id]

    @json_response
    def items(self, request, thing_id):
        return dict(self.root[thing_id].items)

    @json_response
    def item(self, request, thing_id, item_id):
        return self.root[thing_id].items[item_id]

    @json_response
    def set_name(self, request, thing_id):
        name = request.request_json

        with self.transaction_manager:
            thing = self.root[thing_id]
            thing.name = name

        return True

    @json_response
    def tag_add(self, request, thing_id):
        tag = request.request_json

        with self.transaction_manager:
            thing = self.root[thing_id]
            thing.add_tag(tag)

        return set(thing.tags)

    @json_response
    def tag_remove(self, request, thing_id):
        tag = request.request_json

        with self.transaction_manager:
            thing = self.root[thing_id]
            thing.remove_tag(tag)

        return set(thing.tags)

    @json_response
    def online(self, request, thing_id):
        thing = self.root[thing_id]

        return thing.is_online()

    @json_response
    def remove(self, request, thing_id):
        with self.transaction_manager:
            thing = self.root[thing_id]
            thing.bridge.remove_thing(thing)

        return True

    # @json_response
    # def apply(self, request, thing_id, channel_name):
    #     value = request.request_json
    #
    #     return self.root[thing_id].channel(channel_name).apply(value)

    @json_response
    def scan(self, request):
        with self.transaction_manager:
            for bridge in self.root.bridges.values():
                things = bridge.scan()

                for thing in things:
                    bridge.add_thing(thing)

        return True


class ChannelController():
    def __init__(self, app_root, transaction_manager):
        self.root = app_root
        self.transaction_manager = transaction_manager

    @json_response
    def set(self, request, thing_id, channel_name):
        value = request.request_json

        return self.root[thing_id].channel(channel_name).apply(value)

    @json_response
    def on(self, request, thing_id, channel_name):
        return self.root[thing_id].channel(channel_name).on()

    @json_response
    def off(self, request, thing_id, channel_name):
        return self.root[thing_id].channel(channel_name).off()

    @json_response
    def toggle(self, request, thing_id, channel_name):
        return self.root[thing_id].channel(channel_name).toggle()

    # @json_response
    # def items(self, request):
    #     return dict(self.root.items)
    #
    # @json_response
    # def item(self, request, item_id):
    #     return dict(self.root.items)[item_id]
    #
    # @json_response
    # def apply(self, request, item_id):
    #     value = request.request_json
    #
    #     try:
    #         return dict(self.root.items)[item_id].apply(value)
    #     except OfflineException:
    #         return False


class RuleController():
    def __init__(self, app_root, transaction_manager):
        self.root = app_root
        self.transaction_manager = transaction_manager

    @json_response
    def rules(self, request):
        return dict(self.root.rules)

    @json_response
    def rule(self, request, rule_id):
        return self.root.rules[rule_id]

    @json_response
    @log_on_end(logging.INFO, "Added new rule with id \"{result:s}\"", logger=logger)
    def add(self, request):
        rule = Rule(str(uuid.uuid4()), self.root)

        with self.transaction_manager:
            self.root.add_rule(rule)

        return rule.id

    @json_response
    def add_trigger(self, request, rule_id):
        trigger_id = request.request_json

        rule = self.root.rules[rule_id]
        trigger = dict(self.root.triggers)[trigger_id]

        rule.add_trigger(trigger)

        return True


class TriggerController():
    def __init__(self, app_root):
        self.root = app_root

    @json_response
    def triggers(self, request):
        return dict(self.root.triggers)

    @json_response
    def trigger(self, request, trigger_id):
        return dict(self.root.triggers)[trigger_id]


class NotificationController():
    def __init__(self, app_root):
        self.root = app_root

    @json_response
    def notifications(self, request):
        return list(self.root.notifications)

    @json_response
    @log_on_start(logging.INFO, "Removing notification at index {index:d}", logger=logger)
    def remove(self, request, index):
        notification = self.root.notifications[index]
        self.root.delete_notification(notification)

        return True
