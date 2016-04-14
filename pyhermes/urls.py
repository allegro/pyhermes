# -*- coding: utf-8 -*-

from django.conf.urls import url

from pyhermes.subscriber import subscriber


urlpatterns = [
    url(
        r'^events/(?P<subscriber_name>[a-zA-Z0-9_\.-]+)/$',
        subscriber,
        name='hermes-event-subscriber',
    ),
]
