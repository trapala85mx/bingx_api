import time


def get_timestamp(self) -> int:
    """Retorna el timestamp

    Returns:
        int: Entero que representa el timestamp.
    """
    return int(time.time() * 1000)