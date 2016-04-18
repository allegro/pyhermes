from collections import defaultdict

import six

from pyhermes.utils import Singleton
from pyhermes.exceptions import TopicHandlersNotFoundError


class HandlerRegistryMixin(object):
    def __init__(self):
        self.__registry = defaultdict(list)

    def add_handler(self, topic, handler):
        self.__registry[topic].append(handler)

    def get_handlers(self, topic):
        if topic in self.__registry:
            return self.__registry[topic]
        raise TopicHandlersNotFoundError(
            'Handlers for topic {} not found'.format(topic)
        )

    def get_all_handlers(self):
        return self.__registry.copy()


class SubscribersHandlersRegistry(
    six.with_metaclass(Singleton, HandlerRegistryMixin)
):
    """
    Registry of subscription handlers.
    """
    pass


class PublishersHandlersRegistry(
    six.with_metaclass(Singleton, HandlerRegistryMixin)
):
    """
    Registry of publishers.
    """
    pass


SubscribersHandlersRegistry = SubscribersHandlersRegistry()
PublishersHandlersRegistry = PublishersHandlersRegistry()
