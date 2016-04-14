# -*- coding: utf-8 -*-
import json
import logging

from pyhermes.registry import SubscribersHandlersRegistry
from pyhermes.settings import HERMES_SETTINGS

logger = logging.getLogger(__name__)


def handle_subscription(topic, raw_data):
    data = json.loads(raw_data)
    subscribers = SubscribersHandlersRegistry.get_handlers(
        HERMES_SETTINGS.SUBSCRIBERS_MAPPING.get(topic, topic)
    )
    logger.info('`{}` received message: {}'.format(topic, str(data)))
    for subscriber in subscribers:
        subscriber(data)
