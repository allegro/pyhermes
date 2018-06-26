import json
import unittest
from flask import Flask
from ddt import ddt, data as ddt_data, unpack

from pyhermes.apps.flask import configure_pyhermes
from pyhermes.decorators import subscriber


app = Flask(__name__)
app.debug = True
app.config['HERMES'] = {
    'BASE_URL': 'http://hermes.local:8090',
    'SUBSCRIBERS_MAPPING': {'pl.hermes.testTopic': 'new_message'},
    'PUBLISHING_TOPICS': {
        'test1': {
            'description': "test topic",
            'ack': 'LEADER',
            'retentionTime': 1,
            'trackingEnabled': False,
            'contentType': 'JSON',
            'validationEnabled': False,
        }
    }
}
configure_pyhermes(app, url_prefix='/hermes')


@ddt
class SubscriberTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_subscription_with_single_handler(self):
        topic = 'new_message'
        called = [False]
        data = {'a': 'b', 'c': 2}

        @subscriber(topic=topic)
        def subscriber_1(d):
            called[0] = True
            self.assertEqual(d, data)

        response = self.app.post(
            '/hermes/events/pl.hermes.testTopic/',
            data=json.dumps(data),
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(called, [True])

    def test_subscription_with_multiple_handlers(self):
        topic = 'new_message'
        called = [0]
        data = {'a': 'b', 'c': 2}

        @subscriber(topic=topic)
        def subscriber_1(d):
            called[0] = called[0] + 1

        @subscriber(topic=topic)
        def subscriber_2(d):
            called[0] = called[0] + 1

        response = self.app.post(
            '/hermes/events/pl.hermes.testTopic/',
            data=json.dumps(data),
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(called, [2])

    def test_subscription_handler_not_found(self):
        data = {'a': 'b', 'c': 2}
        response = self.app.post(
            '/hermes/events/pl.hermes.topicNotFound/',
            data=json.dumps(data),
        )
        self.assertEqual(response.status_code, 404)

    @unpack
    @ddt_data(
        ('invalid_json',),
    )
    def test_subscription_bad_request(self, data):
        topic = 'new_message'

        @subscriber(topic=topic)
        def subscriber_1(d):
            pass

        response = self.app.post(
            '/hermes/events/pl.hermes.testTopic/',
            data=data,
        )
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
