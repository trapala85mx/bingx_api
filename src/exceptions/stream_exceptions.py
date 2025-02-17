class StreamException(Exception):
    """Clase que representa un error en los Streams"""


class MaxWebsocketConnectionException(StreamException):
    """Representa un error de máximo número de conexiones por IP permitidas"""


class MaxSubscriptionsException(StreamException):
    """Representa un error de máximo número de suscripciones por websocket"""


class ChannelException(StreamException):
    """Representa un error en la construcción del canal."""
