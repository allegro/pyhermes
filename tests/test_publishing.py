# -*- coding: utf-8 -*-
from unittest import TestCase

import responses
from ddt import ddt, data, unpack
from requests.exceptions import ConnectionError, HTTPError, Timeout

from pyhermes.exceptions import HermesPublishException
from pyhermes.publishing import _strip_topic_group, publish
from pyhermes.settings import HERMES_SETTINGS
from pyhermes.utils import override_hermes_settings


def fake_connection_error(request):
    raise ConnectionError('connection error')


def fake_http_error(request):
    raise HTTPError('http error')


def fake_timeout(request):
    raise Timeout('timeout')


TEST_GROUP_NAME = 'pl.allegro.pyhermes'
TEST_TOPIC = 'test-publisher-topic1'
TEST_HERMES_SETTINGS = {
    'BASE_URL': 'http://hermes.local',
    'PUBLISHING_GROUP': {
        'groupName': TEST_GROUP_NAME,
    }
}


@ddt
class PublisherTestCase(TestCase):
    @override_hermes_settings(HERMES=TEST_HERMES_SETTINGS)
    @responses.activate
    @unpack
    @data(
        (201,),
        (202,),
    )
    def test_publish_ok(self, status_code):
        hermes_event_id = 'hermes_ok'
        data = {'test': 'data'}
        responses.add(
            method=responses.POST,
            url="{}/topics/{}.{}".format(
                HERMES_SETTINGS.BASE_URL, TEST_GROUP_NAME, TEST_TOPIC
            ),
            match_querystring=True,
            body=None,
            status=status_code,
            content_type='application/json',
            adding_headers={
                'Hermes-Message-Id': hermes_event_id
            }
        )
        # TODO: check data
        response = publish(TEST_TOPIC, data)
        self.assertEqual(response, hermes_event_id)

    @override_hermes_settings(HERMES=TEST_HERMES_SETTINGS)
    @responses.activate
    def test_publish_full_topic_name(self):
        hermes_event_id = 'hermes_ok'
        data = {'test': 'data'}
        responses.add(
            method=responses.POST,
            url="{}/topics/{}.{}".format(
                HERMES_SETTINGS.BASE_URL, TEST_GROUP_NAME, TEST_TOPIC
            ),
            match_querystring=True,
            body=None,
            status=201,
            content_type='application/json',
            adding_headers={
                'Hermes-Message-Id': hermes_event_id
            }
        )
        # TODO: check data
        response = publish('{}.{}'.format(TEST_GROUP_NAME, TEST_TOPIC), data)
        self.assertEqual(response, hermes_event_id)

    @override_hermes_settings(HERMES=TEST_HERMES_SETTINGS)
    @responses.activate
    @unpack
    @data(
        (200,),
        (400,),
        (403,),
        (404,),
        (500,),
    )
    def test_publish_bad_status_code(self, status_code):
        data = {'test': 'data'}
        responses.add(
            method=responses.POST,
            url="{}/topics/{}.{}".format(
                HERMES_SETTINGS.BASE_URL, TEST_GROUP_NAME, TEST_TOPIC
            ),
            match_querystring=True,
            body=None,
            status=status_code,
            content_type='application/json',
        )
        with self.assertRaises(HermesPublishException) as cm:
            publish(TEST_TOPIC, data)
        self.assertEqual(
            str(cm.exception),
            'Bad response code during Hermes push: {}.'.format(status_code)
        )

    @override_hermes_settings(HERMES=TEST_HERMES_SETTINGS)
    @responses.activate
    @unpack
    @data(
        (fake_connection_error, 'connection error'),
        (fake_http_error, 'http error'),
        (fake_timeout, 'timeout')
    )
    def test_publish_request_error(self, fake_handler, msg):
        data = {'test': 'data'}
        responses.add_callback(
            method=responses.POST,
            url="{}/topics/{}.{}".format(
                HERMES_SETTINGS.BASE_URL, TEST_GROUP_NAME, TEST_TOPIC
            ),
            match_querystring=True,
            content_type='application/json',
            callback=fake_handler,
        )
        with self.assertRaises(HermesPublishException) as cm:
            publish(TEST_TOPIC, data)
        self.assertEqual(
            str(cm.exception),
            'Error pushing event to Hermes: {}.'.format(msg)
        )

    @override_hermes_settings(HERMES=TEST_HERMES_SETTINGS)
    @responses.activate
    def test_publish_request_error_with_retry(self):
        data = {'test': 'data'}
        hermes_event_id = 'hermes_ok'
        tries = [0]

        def callback(request):
            tries[0] += 1
            print(tries)
            if tries[0] <= 2:
                raise ConnectionError('connection error')
            print('Returning normal')
            return (201, {'Hermes-Message-Id': hermes_event_id}, "")

        responses.add_callback(
            method=responses.POST,
            url="{}/topics/{}.{}".format(
                HERMES_SETTINGS.BASE_URL, TEST_GROUP_NAME, TEST_TOPIC
            ),
            match_querystring=True,
            content_type='application/json',
            callback=callback,
        )
        response = publish('{}.{}'.format(TEST_GROUP_NAME, TEST_TOPIC), data)
        self.assertEqual(response, hermes_event_id)
        self.assertEqual(tries[0], 3)

    @override_hermes_settings(HERMES=TEST_HERMES_SETTINGS)
    @responses.activate
    def test_publish_request_wrong_response_code_with_retry(self):
        data = {'test': 'data'}
        hermes_event_id = 'hermes_ok'
        tries = [0]

        def callback(request):
            tries[0] += 1
            if tries[0] <= 2:
                return (408, {}, "")
            return (202, {'Hermes-Message-Id': hermes_event_id}, "")

        responses.add_callback(
            method=responses.POST,
            url="{}/topics/{}.{}".format(
                HERMES_SETTINGS.BASE_URL, TEST_GROUP_NAME, TEST_TOPIC
            ),
            match_querystring=True,
            content_type='application/json',
            callback=callback,
        )
        response = publish('{}.{}'.format(TEST_GROUP_NAME, TEST_TOPIC), data)
        self.assertEqual(response, hermes_event_id)
        self.assertEqual(tries[0], 3)


class TestStripTopicGroupName(TestCase):
    @override_hermes_settings(HERMES=TEST_HERMES_SETTINGS)
    def test_stripping_group_name_when_topic_startswith_group_name(self):
        self.assertEqual(
            _strip_topic_group('pl.allegro.pyhermes.my-topic'),
            'my-topic'
        )

    @override_hermes_settings(HERMES=TEST_HERMES_SETTINGS)
    def test_stripping_group_name_when_topic_not_startswith_group_name(self):
        self.assertEqual(
            _strip_topic_group('my-topic'),
            'my-topic'
        )
