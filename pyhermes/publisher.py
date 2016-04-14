import json
import logging

import requests
from django.conf import settings
from requests.exceptions import ConnectionError, HTTPError, Timeout

from pyhermes.exceptions import HermesPublishException

logger = logging.getLogger(__name__)

HERMES_VALID_RESPONSE_CODES = {201, 202}


def publish(topic, data):
    """
    Push an event to the Hermes.

    Args:
        topic: name of the topic
        data: data to push

    Returns:
        message id from Hermes
    """
    # TODO: try-except
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    url = "{}/topics/{}".format(settings.HERMES['BASE_URL'], topic)
    with requests.Session() as session:
        # TODO - better handling
        # from requests_consul.adapters.service import ConsulServiceAdapter
        # session.mount('service://', ConsulServiceAdapter(
        #     dc=settings.HERMES_CONSUL_DC,
        #     host=settings.HERMES_CONSUL_HOST, port=settings.HERMES_CONSUL_PORT
        # ))
        try:
            resp = session.post(url, headers=headers, data=json_data)
        except (ConnectionError, HTTPError, Timeout) as e:
            message = 'Error pushing event to Hermes: {}.'.format(e)
            logger.exception(message)
            raise HermesPublishException(message)

    if resp.status_code not in HERMES_VALID_RESPONSE_CODES:
        message = 'Bad response code during Hermes push: {}.'.format(
            resp.status_code
        )
        logger.error(message)
        raise HermesPublishException(message)

    hermes_event_id = resp.headers.get('Hermes-Message-Id')
    logger.info('Event sent to Hermes with event_id={}'.format(hermes_event_id))
    return hermes_event_id
