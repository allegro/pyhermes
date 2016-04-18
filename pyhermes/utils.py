# -*- coding: utf-8 -*-
from functools import wraps


class AttributeDict(dict):
    """
    Dict which can handle access to keys using attributes.

    Example:
    >>> ad = AttributeDict({'a': 'b'})
    >>> ad.a
    ... b
    """
    def __init__(self, *args, **kwargs):
        super(AttributeDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class override_hermes_settings(object):
    """
    Utility context manager for overriding pyhermes settings in some context
    (ex. during single test). Could be used as a decorator as well:

    @override_hermes_settings(HERMES={'BASE_URL': 'http://hermes.local'})
    def my_test():
        ...
    """
    def __init__(self, **kwargs):
        self.options = kwargs

    def __enter__(self):
        from pyhermes.settings import HERMES_SETTINGS
        HERMES_SETTINGS._wrapper = self.options

    def __exit__(self, exc_type, exc_value, traceback):
        from pyhermes.settings import HERMES_SETTINGS
        HERMES_SETTINGS._wrapper = None

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper
