class Event(list):
    def __call__(self, *args, **kwargs):
        for listener in self:
            listener(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)


new_thing_found = Event()
