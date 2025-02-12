import hmac
import logging
from hashlib import sha256


class AuthManager:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def get_sign(self, query_string: str, secret_key: str) -> str:
        """
        Crea la singature en base a la query string.
        Args:
            query_string (str): Query string de la petición

        Returns:

        """
        signature = hmac.new(
            secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            digestmod=sha256,
        ).hexdigest()

        return signature
