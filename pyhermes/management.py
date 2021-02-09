import sys

from pyhermes.exceptions import HermesPublishException

TOPICS_ALL = 'all'


def integrations_command_handler(topic, message):
    from pyhermes.publishing import publish
    from pyhermes.settings import HERMES_SETTINGS
    if not HERMES_SETTINGS.ENABLED:
        sys.stderr.write('Hermes integration is disabled. '
                         'Check HERMES.ENABLED variable '
                         'in your settings or environment.')
        return
    if topic == TOPICS_ALL:
        topics = HERMES_SETTINGS.PUBLISHING_TOPICS.keys()
    else:
        topics = [topic]

    if not topics:
        sys.stderr.write('Topics list is empty')

    for topic in topics:
        try:
            sys.stdout.write('Sending message to {}'.format(topic))
            publish(topic, {'result': message})
        except HermesPublishException as e:
            sys.stderr.write(str(e))
        else:
            sys.stdout.write(
                'Message was sent successfully to {}!'.format(topic)
            )
