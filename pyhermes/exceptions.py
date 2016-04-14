class PyhermesException(Exception):
    pass


class HermesPublishException(PyhermesException):
    pass


class TopicHandlersNotFoundError(PyhermesException):
    pass


class PyhermesImproperlyConfiguredError(PyhermesException):
    pass
