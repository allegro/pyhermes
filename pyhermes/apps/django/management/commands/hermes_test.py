# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from pyhermes.management import integrations_command_handler, TOPICS_ALL


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
        topic = options.get('topic')
        message = options.get('message')
        integrations_command_handler(topic, message)
