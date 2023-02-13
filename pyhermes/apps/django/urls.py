# -*- coding: utf-8 -*-
import django

from pyhermes.apps.django.views import subscriber_view


if django.VERSION < (2, 0, 0):
    from django.conf.urls import url
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

else:
    from django.urls import re_path
    urlpatterns = [
        re_path(
            r'^events/(?P<subscriber_name>[a-zA-Z0-9_\.-]+)/$',
            subscriber_view,
            name='hermes-event-subscriber',
        ),
    ]
