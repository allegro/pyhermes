# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from pyhermes.exceptions import HermesPublishException
from pyhermes.publishing import publish
from pyhermes.settings import HERMES_SETTINGS

TOPICS_ALL = 'all'


class Command(BaseCommand):

    help = "Testing integration with Hermes"

    def add_arguments(self, parser):
        parser.add_argument(
            '-m', '--message',
            help='test message',
            default='From pyhermes With Love'
        )
        parser.add_argument(
            '-t', '--topic',
            help='topic',
            default=TOPICS_ALL,
        )

    def handle(self, *args, **options):
        if not HERMES_SETTINGS.ENABLED:
            self.stderr.write(
                'Hermes integration is disabled. '
                'Check HERMES.ENABLED variable '
                'in your settings or environment.'
            )
            return

        topic = options.get('topic')
        message = options.get('message')
        if topic == TOPICS_ALL:
            topics = HERMES_SETTINGS.PUBLISHING_TOPICS.keys()
        else:
            topics = [topic]

        for topic in topics:
            try:
                self.stdout.write('Sending message to {}'.format(topic))
                publish(topic, {'result': message})
            except HermesPublishException as e:
                self.stderr.write(str(e))
            else:
                self.stdout.write(
                    'Message was sent successfully to {}!'.format(topic)
                )
