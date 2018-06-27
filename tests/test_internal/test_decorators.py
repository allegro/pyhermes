#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from pyhermes.decorators import publisher, subscriber
from pyhermes.registry import (
    PublishersHandlersRegistry,
    SubscribersHandlersRegistry
)


@publisher('pl.allegro.pyhermes.topic1')
def publisher1(a, b):
    return a + b


@publisher('pl.allegro.pyhermes.topic1', auto_publish_result=True)
def publisher11(a, b, c):
    return {'result': a + b + c}


@subscriber('pl.allegro.pyhermes.topic1')
def subscriber1(a, b):
    return a + b


@subscriber('pl.allegro.pyhermes.topic1')
def subscriber11(a, b):
    return a + b


class PublisherDecoratorTestCase(unittest.TestCase):
    def test_publishers_registry(self):
        self.assertEqual(
            PublishersHandlersRegistry.get_handlers(
                'pl.allegro.pyhermes.topic1'
            ),
            [publisher1, publisher11]
        )

    def test_subscribers_registry(self):
        self.assertEqual(
            SubscribersHandlersRegistry.get_handlers(
                'pl.allegro.pyhermes.topic1'
            ),
            [subscriber1, subscriber11]
        )

    def test_publisher_set_topic(self):
        self.assertEqual(publisher1._topic, 'pl.allegro.pyhermes.topic1')

    @mock.patch('pyhermes.decorators.publish')
    def test_auto_publish_result(self, publish_mock):
        result = publisher11(2, 3, 4)
        # check if result is still properly returned
        self.assertEqual(result, {'result': 9})
        publish_mock.assert_called_once_with(
            'pl.allegro.pyhermes.topic1', {'result': 9}
        )

    @mock.patch('pyhermes.decorators.publish')
    def test_auto_publish_result_turned_off(self, publish_mock):
        result = publisher1(2, 3)
        # check if result is still properly returned
        self.assertEqual(result, 5)
        self.assertEqual(publish_mock.call_count, 0)
