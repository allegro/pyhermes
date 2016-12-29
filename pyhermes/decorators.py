# -*- coding: utf-8 -*-
from functools import wraps

from pyhermes.registry import (
    PublishersHandlersRegistry,
    SubscribersHandlersRegistry
)
from pyhermes.publishing import _strip_topic_group, publish


class subscriber(object):
    """
    Mark function as subscription handler. Functions decorated with
    `subscriber` decorator will be called automatically by subscription handler

    Usage:
    @subscriber(topic='pl.allegro.pyhermes.topic1')
    def my_subscriber(data):
        ...
    """
    def __init__(self, topic):
        self.topic = topic

    def _get_wrapper(self, func):
        return func

    def __call__(self, func):
        wrapper = self._get_wrapper(func)
        SubscribersHandlersRegistry.add_handler(self.topic, wrapper)
        return wrapper


class publisher(object):
    """
    Mark function as topic publisher.

    Usage:
    @publisher(topic='pl.allegro.pyhermes.topic1')
    def my_publisher():
        ...

    Args:
        * topic - name of Hermes topic (could be with or without group name)
        * auto_publish_result - set to True if result of the function should be
            automatically published to Hermes.
    """
    def __init__(self, topic, auto_publish_result=False):
        self.topic = _strip_topic_group(topic)
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
