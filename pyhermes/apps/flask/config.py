from pyhermes.exceptions import PyhermesImproperlyConfiguredError
from pyhermes.settings import HERMES_SETTINGS


def _load_flask_config(app):
    hermes_settings = app.config.get('HERMES')
    if not hermes_settings:
        raise PyhermesImproperlyConfiguredError('Hermes settings not provided')
    HERMES_SETTINGS.update(**hermes_settings)


def configure_pyhermes(app, url_prefix):
    from pyhermes.apps.flask.blueprints import subscriber_handler  # noqa
    from pyhermes.apps.flask.command import hermes_command  # noqa

    app.cli.add_command(hermes_command)
    app.register_blueprint(subscriber_handler, url_prefix=url_prefix)
    _load_flask_config(app)
