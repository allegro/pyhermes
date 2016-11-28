import json
import logging

import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout

from pyhermes.exceptions import HermesPublishException
from pyhermes.settings import HERMES_SETTINGS
from pyhermes.utils import retry

logger = logging.getLogger(__name__)

HERMES_VALID_RESPONSE_CODES = {201, 202}


def _strip_topic_group(topic):
    """
    Standardize topic name (remove group name from the beginning)
    """
    group_name = HERMES_SETTINGS.PUBLISHING_GROUP['groupName']
    if topic.startswith(group_name):
        topic = topic[len(group_name):]
    return topic


def _get_full_topic_name(topic):
    """

    """
    if not topic.startswith(HERMES_SETTINGS.PUBLISHING_GROUP['groupName']):
        topic = '{}.{}'.format(
            HERMES_SETTINGS.PUBLISHING_GROUP['groupName'], topic
        )
    return topic


def _handle_request_adapter(request_session):
    """
    Handle custom rout-mapping
    See http://docs.python-requests.org/en/master/user/advanced/#transport-adapters  # noqa
    for details
    """
    if HERMES_SETTINGS.URL_ADAPTER:
        request_session.mount(*HERMES_SETTINGS.URL_ADAPTER())


@retry(
    max_attempts=HERMES_SETTINGS.RETRY_MAX_ATTEMTPS,
    retry_exceptions=(HermesPublishException,),
    logger=logger,
)
def _send_message_to_hermes(url, headers, json_data):
    """
    Send message to hermes with retrying.
    """
    with requests.Session() as session:
        _handle_request_adapter(session)
        try:
            resp = session.post(url, headers=headers, data=json_data)
        except (ConnectionError, HTTPError, Timeout) as e:
            message = 'Error pushing event to Hermes: {}.'.format(e)
            raise HermesPublishException(message)

    if resp.status_code not in HERMES_VALID_RESPONSE_CODES:
        message = 'Bad response code during Hermes push: {}.'.format(
            resp.status_code
        )
        raise HermesPublishException(message)
    return resp


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
    if not HERMES_SETTINGS.ENABLED:
        logger.debug('Hermes integration is disabled')
        return
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    url = "{}/topics/{}".format(
        HERMES_SETTINGS.BASE_URL, _get_full_topic_name(topic)
    )
    logger.debug(
        'Pushing message to topic "{}" (url: "{}") with data: {}'.format(
            topic, url, json_data
        )
    )
    try:
        resp = _send_message_to_hermes(url, headers, json_data)
    except HermesPublishException as e:
        message = 'Error pushing event to Hermes: {}.'.format(str(e))
        logger.exception(message)
        raise

    hermes_event_id = resp.headers.get('Hermes-Message-Id')
    logger.info(
        'Event with topic "{}"" sent to Hermes with event_id={}'.format(
            topic, hermes_event_id
        )
    )
    return hermes_event_id
