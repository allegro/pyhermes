# -*- coding: utf-8 -*-
import django
from django.conf.urls import url

from pyhermes.apps.django.views import subscriber_view

urlpatterns = [
    url(
        r'^events/(?P<subscriber_name>[a-zA-Z0-9_\.-]+)/$',
        subscriber_view,
        name='hermes-event-subscriber',
    ),
]

if django.VERSION <= (1, 7):
    from django.conf.urls import patterns
    urlpatterns = patterns('', *urlpatterns)
