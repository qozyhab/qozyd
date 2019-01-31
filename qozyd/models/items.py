# from collections import deque
# from datetime import datetime
#
# from persistent import Persistent
#
# from qozyd.models.channels import Channel
#
#
# class HistoricalValue(Persistent):
#     def __init__(self, value):
#         self.value = value
#         self.date = datetime.now()
#
#     def __json__(self):
#         return {
#             "value": self.value,
#             "date": self.date
#         }
#
#
# class Item(Persistent):
#     def __init__(self, history_size=10):
#         super().__init__()
#
#         self.channel = None
#         self.history = deque(maxlen=history_size)
#
#     def link(self, channel: Channel):
#         if self.channel is not None:
#             self.channel.unlink(self)
#
#         self.channel = channel
#         self.channel.link(self)
#
#     def set(self, value):
#         old_value = self.value
#
#         super().set(value)
#
#         if self._value != value:
#             self.history.append(HistoricalValue(old_value))
#
#         if self.channel:
#             self.channel.apply(value)
#
#
# class Switch(Item):
#     def on(self):
#         self.set(True)
#
#     def off(self):
#         self.set(False)
#
#     def toggle(self):
#         self.set(not self.value)
#
#
# class Number(Item):
#     def __init__(self, *args, step=1, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.step = step
#
#     def increase(self):
#         self.set(self.value + self.step)
#
#     def decrease(self):
#         self.set(self.value - self.step)
#
#
# class Color(Item):
#     pass
#
#
# class Dimmer(Number):
#     pass
#
#
# class Light(Item):
#     def __init__(self, power: Switch, *args, color: Color=None, brightness: Dimmer=None, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.power = power
#         self.color = color
#         self.brightness = brightness
#
#
# # import colorsys
# # from collections import deque
# # from functools import wraps
# # import datetime
# #
# # from persistent import Persistent
# # from persistent.list import PersistentList
# # from persistent.mapping import PersistentMapping
# #
# # from qozyd.utils.units import Unit
# #
# #
# # class Trigger(Persistent):
# #     __parent__ = None
# #
# #     def __init__(self, event_name):
# #         self.event_name = event_name
# #         self.rules = PersistentList()
# #
# #     @property
# #     def id(self):
# #         return ":".join(("trigger", self.__parent__.id, self.event_name))
# #
# #     def add_rule(self, rule):
# #         self.rules.append(rule)
# #
# #     def delete_rule(self, rule):
# #         self.rules.remove(rule)
# #
# #     @property
# #     def __name__(self):
# #         return self.id
# #
# #     def fire(self):
# #         for rule in self.rules:
# #             rule.execute()
# #
# #     def __json__(self):
# #         return {
# #             "id": self.id,
# #             "eventName": self.event_name,
# #             "parent": self.__parent__.id
# #         }
# #
# #
# # class HistoricalValue(Persistent):
# #     def __init__(self, value):
# #         self.value = value
# #         self.date = datetime.datetime.now()
# #
# #     def __json__(self):
# #         return {
# #             "value": self.value,
# #             "date": self.date
# #         }
# #
# #
# # class Item(Persistent):
# #     def __init__(self, thing, channel: Channel=None, sensor: bool=False):
# #         self.__value = None
# #         self.date = None
# #         self.history = deque(maxlen=10)
# #         self.thing = thing
# #         self.channel = channel
# #         self.sensor = sensor
# #         self.triggers = PersistentMapping()
# #
# #         self._add_trigger(Trigger("change"))
# #
# #     def _add_trigger(self, trigger):
# #         trigger.__parent__ = self
# #         self.triggers[trigger.event_name] = trigger
# #
# #     def trigger(self, event_name):
# #         return self.triggers[event_name]
# #
# #     @property
# #     def value(self):
# #         return self.__value
# #
# #     @value.setter
# #     def value(self, value):
# #         if self.value != value:
# #             if self.value is not None:
# #                 # add old value to history
# #                 self.history.append(HistoricalValue(self.value))
# #
# #             self.__value = value
# #             self.date = datetime.datetime.now()
# #
# #             self._p_changed = True
# #
# #             self.trigger("change").fire()
# #
# #     def apply(self, value):
# #         if self.sensor:
# #             raise Exception("Item is in sensor mode")
# #
# #         self.thing.bridge.apply(self.thing, self.channel, value)
# #
# #     @property
# #     def id(self):
# #         return ":".join(("item", self.thing.id, self.channel))
# #
# #     @classmethod
# #     def type_by_name(cls, name):
# #         types_by_name = {
# #             "Switch": Switch,
# #             "Color": Color,
# #             "Dimmer": Dimmer,
# #             "String": String,
# #             "Number": Number,
# #         }
# #
# #         return types_by_name[name]
# #
# #     def __json__(self):
# #         return {
# #             "id": self.id,
# #             "channel": "bla", # self.channel.name,
# #             "sensor": self.sensor,
# #             "type": self.__class__.__name__,
# #             "value": self.value,
# #             "date": datetime.datetime.now(),  # todo: use correct date
# #             "history": list(self.history),
# #         }
# #
# #
# # # Base Items
# #
# # class Switch(Item):
# #     STATUS_ON = True
# #     STATUS_OFF = False
# #
# #     def __init__(self, thing, channel="", sensor=False):
# #         super().__init__(thing, channel, sensor)
# #
# #         self._add_trigger(Trigger("on"))
# #         self._add_trigger(Trigger("off"))
# #
# #     @Item.value.setter
# #     def value(self, value):
# #         if self.value != value:
# #             Item.value.fset(self, value)
# #
# #             if value:
# #                 self.trigger("on").fire()
# #             else:
# #                 self.trigger("off").fire()
# #
# #     @property
# #     def status(self):
# #         return self.value
# #
# #     def on(self):
# #         self.apply(self.STATUS_ON)
# #
# #     def off(self, rpyc):
# #         self.apply(self.STATUS_OFF)
# #
# #     def __json__(self):
# #         return {
# #             **super().__json__(),
# #             # **{
# #             #     "@actions": {
# #             #         "on": {
# #             #             "method": "POST",
# #             #             "url": request.resource_path(self, "on"),
# #             #             "payload": False
# #             #         },
# #             #         "off": {
# #             #             "method": "POST",
# #             #             "url": request.resource_path(self, "off"),
# #             #             "payload": False
# #             #         }
# #             #     }
# #             # }
# #         }
# #
# #
# # class Color(Item):
# #     def rgb(self, rgb):
# #         self.apply(rgb)
# #
# #     @property
# #     def red(self):
# #         return self.value[0]
# #
# #     @property
# #     def green(self):
# #         return self.value[1]
# #
# #     @property
# #     def blue(self):
# #         return self.value[2]
# #
# #     @property
# #     def hls(self):
# #         h, l, s = colorsys.rgb_to_hls(self.red / 255, self.green / 255, self.blue / 255)
# #
# #         return h * 360, l * 100, s * 100
# #
# #     def __json__(self, ):
# #         return {
# #             **super().__json__(),
# #             # **{
# #             #     "@actions": {
# #             #         "setColor": {
# #             #             "method": "POST",
# #             #             "url": request.resource_path(self, "set-color"),
# #             #             "payload": False
# #             #         }
# #             #     }
# #             # }
# #         }
# #
# #
# # class Dimmer(Item):
# #     def dim(self, percentage):
# #         if percentage < 0:
# #             percentage = 0
# #
# #         if percentage > 100:
# #             percentage = 100
# #
# #         self.apply(percentage)
# #
# #     def __json__(self):
# #         return {
# #             **super().__json__(),
# #             # **{
# #             #     "@actions": {
# #             #         "setPercentage": {
# #             #             "method": "POST",
# #             #             "url": request.resource_path(self, "set-percentage"),
# #             #             "payload": True,
# #             #             "payloadSchema": {"type": "number"}
# #             #         }
# #             #     }
# #             # }
# #         }
# #
# #
# # class String(Item):
# #     def __json__(self):
# #         return {
# #             **super().__json__(),
# #             # **{
# #             #     "@actions": {
# #             #         "setValue": {
# #             #             "method": "POST",
# #             #             "url": request.resource_path(self, "set-value"),
# #             #             "payload": True,
# #             #             "payloadSchema": {"type": "string"}
# #             #         }
# #             #     }
# #             # }
# #         }
# #
# #
# # class Number(Item):
# #     def __init__(self, thing, channel: str="", sensor: bool=False, unit: Unit=None):
# #         super().__init__(thing, channel, sensor)
# #
# #         self.unit = unit
# #
# #     def __json__(self):
# #         return {
# #             **super().__json__(),
# #             **{
# #                 "unit_type": self.unit.__class__.__name__ if self.unit else None,
# #                 "unit_symbol": self.unit.unit_symbol if self.unit else None,
# #             }
# #         }
