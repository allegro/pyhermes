import logging
import json
from flask import abort, request, Blueprint
from pyhermes.exceptions import TopicHandlersNotFoundError
from pyhermes.subscription import handle_subscription
from http import HTTPStatus


logger = logging.getLogger(__name__)
subscriber_handler = Blueprint('pyhermes', __name__)


@subscriber_handler.route(
    '/events/<string:subscriber_name>/', methods=['POST']
)
def subscriber_view(subscriber_name):
    raw_data = request.get_data().decode('utf-8')
    event_id = request.headers.get('HTTP_HERMES_MESSAGE_ID')
    retry_count = request.headers.get('HTTP_HERMES_RETRY_COUNT')
    try:
        handle_subscription(subscriber_name, raw_data, event_id, retry_count)
    except TopicHandlersNotFoundError:
        logger.error('subscriber `{}` does not exist.'.format(subscriber_name))
        return abort(HTTPStatus.NOT_FOUND)
    except (ValueError, json.decoder.JSONDecodeError):
        # json loading error
        # TODO: better handling
        return abort(HTTPStatus.BAD_REQUEST)
    else:
        return ('', HTTPStatus.NO_CONTENT)
