# -*- coding: utf-8 -*-
from functools import wraps

from pyhermes.registry import (
    PublishersHandlersRegistry,
    SubscribersHandlersRegistry
)
from pyhermes.publisher import publish


class subscriber(object):
    def __init__(self, topic):
        self.topic = topic

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        SubscribersHandlersRegistry.add_handler(self.topic, wrapper)
        return wrapper


class publisher(object):
    def __init__(self, topic, auto_publish_result=False):
        self.topic = topic
        self.auto_publish_result = auto_publish_result

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if self.auto_publish_result:
                publish(self.topic, result)
            return result
        PublishersHandlersRegistry.add_handler(self.topic, wrapper)
        wrapper._topic = self.topic
        return wrapper
