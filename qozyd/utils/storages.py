class Storable():
    def set(self, value):
        raise NotImplementedError()


class Storage(Storable):
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

#
# class BooleanStorage(Storage):
#     def validate(self, value):
#         if not isinstance(value, bool):
#             raise Exception("Expected value to be of type bool")
#
#
# class NumberStorage(Storage):
#     def __init__(self, min=None, max=None):
#         super().__init__()
#
#         self.min = min
#         self.max = max
#
#     def validate(self, value):
#         if self.min and value < self.min:
#             raise Exception("{:d} smaller than minimum value of {:d}".format(value, self.min))
#
#         if self.max and value > self.max:
#             raise Exception("{:d} bigger than maximum value of {:d}".format(value, self.max))
