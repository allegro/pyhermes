# -*- coding: utf-8 -*-
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from pyhermes.exceptions import TopicHandlersNotFoundError
from pyhermes.subscription import handle_subscription

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def subscriber_view(request, subscriber_name):
    raw_data = request.read().decode('utf-8')
    event_id = request.META.get('HTTP_HERMES_MESSAGE_ID')
    retry_count = request.META.get('HTTP_HERMES_RETRY_COUNT')
    try:
        handle_subscription(subscriber_name, raw_data, event_id, retry_count)
    except TopicHandlersNotFoundError:
        logger.error('subscriber `{}` does not exist.'.format(subscriber_name))
        return HttpResponse(status=404)
    except ValueError:
        # json loading error
        # TODO: better handling
        return HttpResponse(status=400)
    else:
        return HttpResponse(status=204)
