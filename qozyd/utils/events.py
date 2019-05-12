# import fnmatch
# from collections import defaultdict
#
#
# class EventBus():
#     def __init__(self):
#         self.listeners = defaultdict(list)
#
#     def dispatch(self, event, *args, **kwargs):
#         for listen_event, listeners in self.listeners:
#             if fnmatch.fnmatch(event, listen_event):
#                 for listener in listeners:
#                     listener(*args, **kwargs)
#
#     def listen(self, event, callback):
#         self.listeners[event].append(callback)
#
# 
# event_bus = EventBus()
#

class Event(list):
    async def __call__(self, *args, **kwargs):
        for listener in self:
            await listener(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)


new_thing_found = Event()
