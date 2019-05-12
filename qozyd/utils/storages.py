from qozyd.utils.events import Event


class Storage():
    def __init__(self):
        self._value = None
        self.on_change = Event()

    @property
    def value(self):
        return self._value

    def ensure_valid(self, valid, validation_message):
        if not valid:
            raise Exception(validation_message)

    def validate(self, value):
        pass

    async def set(self, value):
        self.validate(value)

        old_value = self._value
        self._value = value

        if old_value != value:
            await self.on_change(value, old_value)
