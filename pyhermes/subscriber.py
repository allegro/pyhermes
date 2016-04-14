# -*- coding: utf-8 -*-
import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from pyhermes.exceptions import TopicHandlersNotFoundError
from pyhermes.registry import SubscribersHandlersRegistry
from pyhermes.settings import HERMES_SETTINGS

logger = logging.getLogger(__name__)


# TODO: move it to django handler
@csrf_exempt
@require_POST
def subscriber_view(request, subscriber_name):
    raw_data = request.read().decode('utf-8')
    try:
        handle_subscription(subscriber_name, raw_data)
    except TopicHandlersNotFoundError:
        logger.error('subscriber `{}` does not exist.'.format(subscriber_name))
        return HttpResponse(status=404)
    except ValueError:
        # json loading error
        # TODO: better handling
        return HttpResponse(status=400)
    else:
        return HttpResponse(status=204)


def handle_subscription(topic, raw_data):
    data = json.loads(raw_data)
    subscribers = SubscribersHandlersRegistry.get_handlers(
        HERMES_SETTINGS.SUBSCRIBERS_MAPPING.get(topic, topic)
    )
    logger.info('`{}` received message: {}'.format(topic, str(data)))
    for subscriber in subscribers:
        subscriber(data)
