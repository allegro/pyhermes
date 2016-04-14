# -*- coding: utf-8 -*-
import responses
from ddt import ddt, data, unpack
from django.conf import settings
from django.test import override_settings, TestCase
from requests.exceptions import ConnectionError, HTTPError, Timeout

from pyhermes.exceptions import HermesPublishException
from pyhermes.publisher import publish


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
    @override_settings(HERMES=TEST_HERMES_SETTINGS)
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
                settings.HERMES['BASE_URL'], TEST_GROUP_NAME, TEST_TOPIC
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

    @override_settings(HERMES=TEST_HERMES_SETTINGS)
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
                settings.HERMES['BASE_URL'], TEST_GROUP_NAME, TEST_TOPIC
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

    @override_settings(HERMES=TEST_HERMES_SETTINGS)
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
                settings.HERMES['BASE_URL'], TEST_GROUP_NAME, TEST_TOPIC
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
