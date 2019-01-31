import colorsys

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

    def apply(self, value):
        if self.sensor:
            raise Exception("Channel is in sensor mode!")

        self.validate(value)

        self.thing.bridge.apply(self.thing, self, value)

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
        self.set(True)

    def off(self):
        self.set(False)

    def toggle(self):
        self.set(not self.value)


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

        self.set(self.value + step)

    def decrease(self):
        step = self.step or 1

        self.set(self.value - step)


class StringChannel(Channel):
    TYPE_NAME = "String"

    def validate(self, value):
        self.ensure_valid(isinstance(value, str), "{:s} is not of type string".format(str(value.__class__)))


class Color():
    @staticmethod
    def from_rgb(self, r, g, b):
        raise NotImplementedError

    def rgb(self):
        raise NotImplementedError

    def convert(self, target):
        return target.from_rgb(*self.rgb())


class RGB(Color):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def from_rgb(cls, r, g, b):
        return RGB(r, g, b)

    def rgb(self):
        return self.r, self.g, self.b

    def convert(self, target):
        return target.from_rgb(self.r, self.g, self.b)


class HSV(Color):
    def __init__(self, h, s, v):
        self.h = h
        self.s = s
        self.v = v

    @classmethod
    def from_rgb(cls, r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

        return HSV(h * 360, s * 100, v * 100)

    def rgb(self):
        r, g, b = colorsys.hsv_to_rgb(self.h / 360.0, self.s / 100.0, self.v / 100.0)

        return int(r * 255), int(g * 255), int(b * 255)


class HSL(Color):
    def __init__(self, h, s, l):
        self.h = h
        self.s = s
        self.l = l

    @classmethod
    def from_rgb(cls, r, g, b):
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

        return HSL(h * 360, s * 100, l * 100)

    def rgb(self):
        r, g, b = colorsys.hls_to_rgb(self.h / 360.0, self.l / 100.0, self.s / 100.0)

        return int(r * 255), int(g * 255), int(b * 255)


class ColorChannel(Channel):
    TYPE_NAME = "Color"

    def validate(self, value):
        self.ensure_valid(isinstance(value, Color), "Invalid color value {:s}".format(str(value)))

    def get_as(self, color_space):
        if self.value:
            return self.value.convert(color_space)

        return None
