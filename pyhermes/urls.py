# -*- coding: utf-8 -*-

from django.conf.urls import url

from pyhermes.subscriber import subscriber_view

# TODO: move it to django handler
urlpatterns = [
    url(
        r'^events/(?P<subscriber_name>[a-zA-Z0-9_\.-]+)/$',
        subscriber_view,
        name='hermes-event-subscriber',
    ),
]
