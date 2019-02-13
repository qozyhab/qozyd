class Storage():
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    def ensure_valid(self, valid, validation_message):
        if not valid:
            raise Exception(validation_message)

    def validate(self, value):
        pass

    def set(self, value):
        self.validate(value)

        self._value = value
