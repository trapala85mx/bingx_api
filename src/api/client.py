import logging
from typing import Any, Dict, Optional

from src.models.request_model import RequestModel
from src.utils.const import Endpoints, HttpMethod
from src.utils.http_manager import HttpManager


class Perpetual:
    """Clase que interactúa con los Futuros Perpetuos de Bingx."""

    BASE_URL = Endpoints.BASE_URL

    def __init__(
        self, api_key: Optional[str] = None, secret: Optional[str] = None
    ) -> None:
        self.api_key = api_key
        self.secret_key = secret
        self.headers = {"X-BX-APIKEY": self.api_key}
        self.http_manager = HttpManager()
        self.logger = logging.getLogger(__name__)

    async def server_timestamp(self) -> int:
        """
        Obtiene la hora desde el servidor.
        Returns (int): Timestamp del servidor.
        """
        endpoint = Endpoints.SERVER_TIMESTAMP
        method = HttpMethod.GET
        url = f"{Perpetual.BASE_URL}{endpoint}"
        signed = False

        params = None
        data = None

        request_data = RequestModel(
            method=method,
            url=url,
            params=params if params else {},
            data=data if data else {},
            login=signed,
        )

        response = await self.http_manager.make_request(request_data=request_data)

        return response["data"]["serverTime"]

    async def _get_body_data(self, params: Dict[str, Any]) -> Dict[str, Any]: ...
