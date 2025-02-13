import hmac
import time
import urllib
from hashlib import sha256
from typing import Any, Dict


async def params_str(params: Dict[str, Any]) -> str:
    """
    Convierte los parámetros en query string.
    Args:
        params (Dict[str, Any]): Parámetros de la petición.

    Returns:
        (str): Parámetros en cadena texto url encodeados.

    Raises:
        ApiException: Error dentro de la API.
    """
    params["timestamp"] = str(await get_timestamp())
    # Ordenar los parámetros para la firma
    sorted_params = dict(sorted(params.items()))
    param_str = urllib.parse.urlencode(
        sorted_params, safe='{}":,'
    )  # Mantener los caracteres de JSON seguros
    return param_str


async def get_timestamp() -> int:
    """
    Obtiene el timestamp actual.

    Returns:
        (int): Entero que representa el timestamp.

    Raises:
        ApiException: Error dentro de la API.
    """
    return int(time.time() * 1_000)


async def get_sign(param_str: str, secret: str) -> str:
    """
    Crea la singature de los peticiones que necesitan auth.
    Args:
        param_str (str): Query string a enviar en la URL.
        secret (str): secret key to encode.
    Returns:
        (str): Cadena de texto de la signature.
    Raises:
        ApiException: Error dentro de la API.
    """
    signature = hmac.new(
        secret.encode("utf-8"),
        param_str.encode("utf-8"),
        digestmod=sha256,
    ).hexdigest()
    return signature
