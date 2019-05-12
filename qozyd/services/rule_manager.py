from qozyd.context import AsyncContextExecutable


class RuleManager(AsyncContextExecutable):
    def __init__(self, qozy, transaction_manager, bridge_manager):
        self.qozy = qozy
        self.transaction_manager = transaction_manager
        self.bridge_manager = bridge_manager

        self.compiled_rules = {}

    async def start(self):
        for rule in self.qozy.rules.values():
            self.compiled_rules[rule.id] = await rule.compile(self.bridge_manager)

            await self.compiled_rules[rule.id].activate()

    async def reload(self, rule):
        if rule.id in self.compiled_rules:
            await self.compiled_rules[rule.id].deactivate()

        self.compiled_rules[rule.id] = await rule.compile(self.bridge_manager)
        await self.compiled_rules[rule.id].activate()

    async def remove(self, rule):
        with self.transaction_manager:
            if rule.id in self.compiled_rules:
                await self.compiled_rules[rule.id].deactivate()
                del self.compiled_rules[rule.id]

            self.qozy.delete_rule(rule)

    async def execute(self, rule):
        if rule.id in self.compiled_rules:
            await self.compiled_rules[rule.id].execute()
            return True

        raise Exception("Uncompiled rule")
