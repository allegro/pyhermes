# -*- coding: utf-8 -*-
import json
import logging

from pyhermes.registry import SubscribersHandlersRegistry
from pyhermes.settings import HERMES_SETTINGS

logger = logging.getLogger(__name__)


def handle_subscription(topic, raw_data, event_id, retry_count):
    """
    Handler for topic subscription. Should be exposed (and possibly wrapped)
    through HTTP endpoint in chosen framework.

    Args:
        * topic: name of Hermes topic
        * raw_data: string with raw data for event
        * event_id: id of Hermes event
        * retry_count: number of retries to deliver this event
          (counting from 0)
    """
    if not HERMES_SETTINGS.ENABLED:
        logger.debug('Hermes integration is disabled')
        return
    data = json.loads(raw_data)
    subscribers = SubscribersHandlersRegistry.get_handlers(
        HERMES_SETTINGS.SUBSCRIBERS_MAPPING.get(topic, topic)
    )
    logger.info((
        'Received message for topic "{}" (eventID: {}, retry count: {})'
    ).format(topic, event_id, retry_count))
    logger.debug('Message data {}'.format(str(data)))
    for subscriber in subscribers:
        subscriber(data)
