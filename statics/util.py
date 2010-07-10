""" Utilities."""

__all__ = ["cached_property", "cached_generator_property"]


class cached_property(object):

    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def compute_value(self, obj):
        return self.func(obj)

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.compute_value(obj)
        obj.__dict__[self.__name__] = value
        return value


class cached_generator_property(cached_property):

    def compute_value(self, obj):
        return list(self.func(obj))
