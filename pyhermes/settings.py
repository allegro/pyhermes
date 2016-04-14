"""
"""
from django.conf import settings

from pyhermes.exceptions import PyhermesImproperlyConfiguredError

_DEFAULT_GROUP_NAME = '__default__'
DEFAULTS = {
    'BASE_URL': '',
    'URL_ADAPTER': None,
    'PUBLISHING_GROUP': {
        'groupName': _DEFAULT_GROUP_NAME,
    },
    'PUBLISHING_TOPICS': {},
    'SUBSCRIBERS_MAPPING': {},
}


class HermesSettings(object):
    def __getattr__(self, attr):
        try:
            return getattr(settings, 'HERMES', {})[attr]
        except KeyError:
            return DEFAULTS[attr]

HERMES_SETTINGS = HermesSettings()


def _validate_hermes_settings(hermes_settings):
    if not hermes_settings.BASE_URL:
        raise PyhermesImproperlyConfiguredError('Hermes BASE_URL not provided')
    if (
        not hermes_settings.PUBLISHING_GROUP or
        hermes_settings.PUBLISHING_GROUP['groupName'] == _DEFAULT_GROUP_NAME
    ):
        raise PyhermesImproperlyConfiguredError(
            'Hermes GROUP info not provided'
        )

# _validate_hermes_settings(HERMES_SETTINGS)
