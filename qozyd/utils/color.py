import colorsys


class Color():
    @staticmethod
    def from_rgb(self, r, g, b):
        raise NotImplementedError

    def rgb(self):
        raise NotImplementedError

    def convert(self, target):
        return target.from_rgb(*self.rgb())

    def __json__(self):
        return self.rgb()


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

        return round(r * 255), round(g * 255), round(b * 255)


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

        return round(r * 255), round(g * 255), round(b * 255)
