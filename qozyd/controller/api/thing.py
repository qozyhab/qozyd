from aiohttp import web

from qozyd.controller import Controller
from qozyd.http.decorator import json_response


class ThingController(Controller):
    def __init__(self, app_root, transaction_manager, bridge_manager):
        self.root = app_root
        self.transaction_manager = transaction_manager
        self.bridge_manager = bridge_manager

    @json_response
    async def things(self, request):
        things = dict(self.root.things)

        expand = request.query.getone("expand", False)
        filter_tags = request.query.getall("tag", None)

        if filter_tags:
            things = {id: thing for id, thing in things.items() if any(tag in filter_tags for tag in thing.tags)}

        if expand:
            return things

        return list(things.keys())

    @json_response
    async def tags(self, request):
        things = dict(self.root.things)

        tags = set()

        for thing in things.values():
            tags = tags.union(thing.tags)

        return tags

    @json_response
    async def thing(self, request):
        thing_id = request.match_info.get("thing_id")

        return self.root[thing_id]

    @json_response
    async def channels(self, request):
        thing_id = request.match_info.get("thing_id")

        return dict(self.root[thing_id].channels)

    @json_response
    async def channel(self, request):
        thing_id = request.match_info.get("thing_id")
        channel_name = request.match_info.get("channel_name")

        return self.root[thing_id].channel(channel_name)

    @json_response
    async def set_name(self, request):
        thing_id = request.match_info.get("thing_id")

        name = await request.json()

        with self.transaction_manager:
            thing = self.root[thing_id]
            thing.name = name

        return True

    @json_response
    async def tag_add(self, request):
        thing_id = request.match_info.get("thing_id")

        tag = await request.json()

        with self.transaction_manager:
            thing = self.root[thing_id]
            thing.add_tag(tag)

        return set(thing.tags)

    @json_response
    async def tag_remove(self, request):
        thing_id = request.match_info.get("thing_id")

        tag = await request.json()

        with self.transaction_manager:
            thing = self.root[thing_id]
            thing.remove_tag(tag)

        return set(thing.tags)

    @json_response
    async def online(self, request):
        thing_id = request.match_info.get("thing_id")

        thing = self.root[thing_id]

        return self.bridge_manager.is_online(thing)

    @json_response
    async def remove(self, request):
        thing_id = request.match_info.get("thing_id")

        with self.transaction_manager:
            thing = self.root[thing_id]
            thing.bridge.remove_thing(thing)

        return True

    @json_response
    async def scan(self, request):
        new_things = await self.bridge_manager.scan()

        return new_things

    @json_response
    async def find(self, request):
        await self.bridge_manager.find()

        return True

    def routes(self):
        return [
            web.get("/api/things", self.things),
            web.get("/api/things/scan", self.scan),
            web.get("/api/things/find", self.find),
            web.get("/api/things/tags", self.tags),
            web.get("/api/things/{thing_id}", self.thing),
            web.delete("/api/things/{thing_id}", self.remove),
            web.get("/api/things/{thing_id}/channels", self.channels),
            web.get("/api/things/{thing_id}/channels/{channel_name}", self.channel),
            web.put("/api/things/{thing_id}/name", self.set_name),
            web.post("/api/things/{thing_id}/tags", self.tag_add),
            web.delete("/api/things/{thing_id}/tags", self.tag_remove),
            web.get("/api/things/{thing_id}/online", self.online),
        ]
