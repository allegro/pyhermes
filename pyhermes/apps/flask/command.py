import click
from flask.cli import AppGroup
from pyhermes.management import integrations_command_handler, TOPICS_ALL


hermes_command = AppGroup('hermes')


@hermes_command.command('test')
@click.option(
    '-t', '--topic',
    help='topic',
    default=TOPICS_ALL,
)
@click.option(
    '-m', '--message',
    help='test message',
    default='From pyhermes With Love'
)
def test_hermes_command(topic, message):
    integrations_command_handler(topic, message)
