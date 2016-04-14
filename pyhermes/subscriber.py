# -*- coding: utf-8 -*-
import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from pyhermes.exceptions import TopicHandlersNotFoundError
from pyhermes.registry import SubscribersHandlersRegistry
from pyhermes.settings import HERMES_SETTINGS

HERMES_SUBSCRIBERS_MAPPING = HERMES_SETTINGS['SUBSCRIBERS_MAPPING']

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def subscriber(request, subscriber_name):
    try:
        subscribers = SubscribersHandlersRegistry.get_handlers(
            HERMES_SUBSCRIBERS_MAPPING.get(subscriber_name, subscriber_name)
        )
    except TopicHandlersNotFoundError:
        logger.error('subscriber `{}` does not exist.'.format(subscriber_name))
        return HttpResponse(status=404)
    else:
        raw_data = request.read().decode('utf-8')
        try:
            data = json.loads(raw_data)
        except ValueError:
            return HttpResponse(status=400)
        logger.info('`{}` received message: {}'.format(
            subscriber_name, str(data)
        ))
        for subscriber in subscribers:
            subscriber(data)
        return HttpResponse(status=204)
