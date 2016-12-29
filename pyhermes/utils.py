# -*- coding: utf-8 -*-
import logging
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


# TODO(mkurek): add delay between consecutive retries
class retry(object):
    """
    Decorator providing retrying in case of error in wrapped function.

    Args:
        * max_attempts (int) - maximum number of retries
        * retry_exceptions (iterable) - exceptions, on which retry should
          happen
        * logger (Logger) - instance of python Logger

    Usage:
    @retry(max_attempts=4, retryExceptions=[ValueError])
    def send_data(url, data):
        ...
    """
    def __init__(self, max_attempts=1, retry_exceptions=None, logger=None):
        self.max_attempts = max_attempts
        assert self.max_attempts > 0
        self.retry_exceptions = retry_exceptions or (Exception,)
        self.logger = logger or logging.getLogger(__name__)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tries_left = self.max_attempts
            while tries_left > 1:
                tries_left -= 1
                try:
                    return func(*args, **kwargs)
                except self.retry_exceptions as e:
                    msg = 'Retrying because of {}'.format(str(e))
                    self.logger.warning(msg)
            return func(*args, **kwargs)
        return wrapper
