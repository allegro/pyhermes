# -*- coding: utf-8 -*-
import json

from ddt import ddt, data as ddt_data, unpack
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from pyhermes.decorators import subscriber


@ddt
class SubscriberTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_subscription_with_single_handler(self):
        topic = 'pl.allegro.pyhermes.test-subscriber-topic1'
        called = [False]
        data = {'a': 'b', 'c': 2}

        @subscriber(topic=topic)
        def subscriber_1(d):
            called[0] = True
            self.assertEqual(d, data)

        response = self.client.post(
            reverse('hermes-event-subscriber', args=(topic,)),
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(called, [True])

    def test_subscription_with_multiple_handlers(self):
        topic = 'pl.allegro.pyhermes.test-subscriber-topic2'
        called = [0]
        data = {'a': 'b', 'c': 2}

        @subscriber(topic=topic)
        def subscriber_1(d):
            called[0] = called[0] + 1

        @subscriber(topic=topic)
        def subscriber_2(d):
            called[0] = called[0] + 1

        response = self.client.post(
            reverse('hermes-event-subscriber', args=(topic,)),
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(called, [2])

    def test_subscription_handler_not_found(self):
        topic = 'pl.allegro.pyhermes.test-subscriber-handler-not-found'
        data = {'a': 'b', 'c': 2}
        response = self.client.post(
            reverse('hermes-event-subscriber', args=(topic,)),
            data=json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    @unpack
    @ddt_data(
        ('invalid_json',),
    )
    def test_subscription_bad_request(self, data):
        topic = 'pl.allegro.pyhermes.test-subscriber-topic3'

        @subscriber(topic=topic)
        def subscriber_1(d):
            pass

        response = self.client.post(
            reverse('hermes-event-subscriber', args=(topic,)),
            data=data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
