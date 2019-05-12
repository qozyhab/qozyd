import uuid

import logging
from aiohttp import web

from qozyd.controller import Controller
from qozyd.http.decorator import json_response
from qozyd.http.utils import get_or_404
from qozyd.models.rules import ScriptRule
from qozyd.utils.json import json_encode

logger = logging.getLogger(__name__)


class RuleController(Controller):
    def __init__(self, app_root, transaction_manager, bridge_manager, rule_manager):
        self.root = app_root
        self.transaction_manager = transaction_manager
        self.bridge_manager = bridge_manager
        self.rule_manager = rule_manager

    @json_response
    async def rules(self, request):
        return list(self.root.rules.keys())

    @json_response
    async def rule(self, request):
        rule_id = request.match_info.get("rule_id")

        return get_or_404(self.root.rules, rule_id)

    @json_response
    async def rule_condition(self, request):
        rule_id = request.match_info.get("rule_id")

        rule = get_or_404(self.root.rules, rule_id)

        return rule.condition.evaluate(self.root)

    @json_response
    async def rule_execute(self, request):
        rule_id = request.match_info.get("rule_id")

        rule = get_or_404(self.root.rules, rule_id)

        return await self.rule_manager.execute(rule)

    @json_response
    async def patch_rule(self, request):
        rule_id = request.match_info.get("rule_id")

        rule = get_or_404(self.root.rules, rule_id)

        with self.transaction_manager as transaction:
            rule.patch(await request.json())

            if not rule.is_valid():
                errors = rule.validation_errors()
                transaction.abort()

                raise web.HTTPUnprocessableEntity(text=json_encode(errors), content_type="application/json")

        await self.rule_manager.reload(rule)

        return True

    @json_response
    # @log_on_end(logging.INFO, "Added new rule with id \"{result:s}\"", logger=logger)
    async def add_script_rule(self, request):
        rule = ScriptRule(str(uuid.uuid4()), self.root)

        with self.transaction_manager:
            self.root.add_rule(rule)

        return rule.id

    @json_response
    async def remove_rule(self, request):
        rule_id = request.match_info.get("rule_id")

        rule = get_or_404(self.root.rules, rule_id)

        await self.rule_manager.remove(rule)

        return True

    def routes(self):
        return [
            web.get("/api/rules", self.rules),
            web.get("/api/rules/{rule_id}", self.rule),
            web.get("/api/rules/{rule_id}/condition", self.rule_condition),
            web.get("/api/rules/{rule_id}/execute", self.rule_execute),
            web.patch("/api/rules/{rule_id}", self.patch_rule),
            web.post("/api/rules/script", self.add_script_rule),
            web.delete("/api/rules/{rule_id}", self.remove_rule)
        ]
