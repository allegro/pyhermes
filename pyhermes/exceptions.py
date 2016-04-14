class DjangoHermesException(Exception):
    pass


class HermesPublishException(DjangoHermesException):
    pass


class TopicHandlersNotFoundError(DjangoHermesException):
    pass
