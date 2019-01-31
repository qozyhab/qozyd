from enum import Enum


class Unit(Enum):
    def __init__(self, unit_symbol, base_divisor):
        self.unit_symbol = unit_symbol
        self.base_divisor = base_divisor

    def convert(self, value, unit):
        assert self.__class__ is unit.__class__

        return value * self.base_divisor / unit.base_divisor 


class Length(Unit):
    CENTIMETER = ("cm", 1)
    METER = ("m", 100)
    KILOMETER = ("km", 10000)
    INCH = ("in", 2.54)
    FEET = ("ft", 30.48)
    MILES = ("mi", 160934)


class Temperature(Unit):
    CELSIUS = ("°C", 1)
    FAHRENHEIT = ("F", 33.8)
    KELVIN = ("K", 274.15)


class Percentage(Unit):
    PERCENT = ("%", 1)
    PER_MILL = ("‰", 0.1)
