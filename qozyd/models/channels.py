from qozyd.utils.color import Color
from qozyd.utils.storages import Storage
from persistent.persistence import Persistent


class Channel(Persistent, Storage):
    TYPE_NAME = None

    def __init__(self,
                 thing,
                 name: str,
                 sensor: bool=False,
                 settings: dict=None):
        super().__init__()

        self.thing = thing
        self.name = name
        self.sensor = sensor
        self.settings = settings

    @property
    def id(self):
        return ":".join((self.thing.id, self.name))

    # def apply(self, value):
    #     if self.sensor:
    #         raise Exception("Channel is in sensor mode!")
    #
    #     self.validate(value)
    #
    #     self.thing.bridge.apply(self.thing, self, value)
    #
    #     return True

    @classmethod
    def type_by_name(cls, name):
        return {
            SwitchChannel.TYPE_NAME: SwitchChannel,
            NumberChannel.TYPE_NAME: NumberChannel,
            StringChannel.TYPE_NAME: StringChannel,
            ColorChannel.TYPE_NAME: ColorChannel
        }[name]

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "sensor": self.sensor,
            "type": self.__class__.__name__,
            "value": self.value,
        }


class SwitchChannel(Channel):
    TYPE_NAME = "Switch"

    def validate(self, value):
        self.ensure_valid(isinstance(value, bool), "Value must be of type bool")

    def on(self):
        return self.apply(True)

    def off(self):
        return self.apply(False)

    def toggle(self):
        return self.apply(not self.value)


class NumberChannel(Channel):
    TYPE_NAME = "Number"

    def __init__(self, *args, min=None, max=None, step=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.min = min
        self.max = max
        self.step = step

    def validate(self, value):
        if self.min:
            self.ensure_valid(self.min <= value, "{:d} is smaller than minimum value of {:d}".format(value, self.min))

        if self.max:
            self.ensure_valid(self.max >= value, "{:d} is bigger than maximum value of {:d}".format(value, self.max))

    def increase(self):
        step = self.step or 1

        return self.apply(self.value + step)

    def decrease(self):
        step = self.step or 1

        return self.apply(self.value - step)


class StringChannel(Channel):
    TYPE_NAME = "String"

    def validate(self, value):
        self.ensure_valid(isinstance(value, str), "{:s} is not of type string".format(str(value.__class__)))


class ColorChannel(Channel):
    TYPE_NAME = "Color"

    def validate(self, value):
        self.ensure_valid(isinstance(value, Color), "Invalid color value {:s}".format(str(value)))

    def get_as(self, color_space):
        if self.value:
            return self.value.convert(color_space)

        return None
