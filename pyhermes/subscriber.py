# -*- coding: utf-8 -*-
import json
import logging

from pyhermes.registry import SubscribersHandlersRegistry
from pyhermes.settings import HERMES_SETTINGS

logger = logging.getLogger(__name__)


def handle_subscription(topic, raw_data):
    """
    Handler for topic subscription. Should be exposed (and possibly wrapped)
    through HTTP endpoint in chosen framework.

    Args:
        * topic: name of Hermes topic
        * raw_data: string with raw data for event
    """
    if not HERMES_SETTINGS.ENABLED:
        logger.debug('Hermes integration is disabled')
        return
    data = json.loads(raw_data)
    subscribers = SubscribersHandlersRegistry.get_handlers(
        HERMES_SETTINGS.SUBSCRIBERS_MAPPING.get(topic, topic)
    )
    logger.info('`{}` received message: {}'.format(topic, str(data)))
    for subscriber in subscribers:
        subscriber(data)
