import hmac
import logging
import time
import urllib
from hashlib import sha256
from typing import Any, Dict, Optional

import aiohttp.http
import pydantic_core

from src.exceptions.api_exceptions import ApiException
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
        self.session = aiohttp.ClientSession()
        self.headers = {"X-BX-APIKEY": self.api_key}
        self.http_manager = HttpManager()
        self.logger = logging.getLogger(__name__)

    async def close(self):
        await self.session.close()

    async def server_timestamp(self) -> Any | None:
        """
        Obtiene la hora desde el servidor.

        Returns (int): Timestamp del servidor.

        Raises:
            ApiException: Error dentro de la API.
        """
        endpoint = Endpoints.SERVER_TIMESTAMP
        url = f"{Perpetual.BASE_URL}{endpoint}"

        try:
            request_data = RequestModel(
                method=HttpMethod.GET,
                url=url,
                login=False,
            )

            response = await self._make_request(request_data=request_data)

            return response["data"]["serverTime"]

        except pydantic_core.ValidationError as err:
            self.logger.critical(
                "Error de Pydantic al crear el RequestModel: %s", str(err)
            )
            raise ApiException(f"Error en Pydantic: {str(err)}") from err

    async def contracts(self, symbol: Optional[str] = None) -> Dict[str, Any] | None:
        """
        Arma lo neceasrio para realizar la petición al endpoint para traer la información de los contratos
        Args:
            symbol (Optional[Dict[str,Any]]): Ticker symbol del activo del cual se quiere obtener la info. Default. None

        Returns:
            Dict[str,Any]: Respuesta del Servidor.

        Raises:
            ApiException: Error dentro de la API.
        """
        endpoint = Endpoints.CONTRACTS
        url = f"{Perpetual.BASE_URL}{endpoint}"
        params = None

        if symbol:
            if len(symbol) > 0:
                params["symbol"] = symbol
        try:
            request_data = RequestModel(
                method=HttpMethod.GET,
                url=url,
                login=False,
                params=params,
            )

            response = await self._make_request(request_data=request_data)

            return response
        except pydantic_core.ValidationError as err:
            self.logger.critical(
                "Error de Pydantic al crear el RequestModel: %s", str(err)
            )
            raise ApiException(f"Error en Pydantic: {str(err)}") from err

    async def kline_data(self, symbol: str, interval: str, **kwargs) -> Dict[str, Any]:
        path = Endpoints.KLINES
        url = f"{Perpetual.BASE_URL}{path}"
        params = {"symbol": symbol, "interval": interval}
        start = kwargs.get("start", None)
        end = kwargs.get("end", None)

        if start:
            params["startTime"] = start
        if end:
            params["endTime"] = end

        try:
            request_data = RequestModel(
                method=HttpMethod.GET,
                url=url,
                params=params,
                login=False,
            )

            response = await self._make_request(request_data=request_data)

            return response

        except pydantic_core.ValidationError as err:
            self.logger.debug(
                "Error de Pydantic al crear el RequestModel: %s", str(err)
            )
            raise ApiException(f"Error en Pydantic: {str(err)}") from err

    async def account_data(self) -> Dict[str, Any]:
        path = Endpoints.ACCOUNT
        url = f"{Perpetual.BASE_URL}{path}"

        try:
            request_data = RequestModel(
                method=HttpMethod.GET,
                login=True,
                url=url,
            )

            response = await self._make_request(request_data)
            return response

        except pydantic_core.ValidationError as e:
            self.logger.critical(
                "Error de Pydantic al crear el RequestModel: %s", str(e)
            )
            raise ApiException(f"Error en Pydantic: {str(e)}") from e

    async def query_margin_type(self, symbol: str) -> Dict[str, Any]:
        path = Endpoints.QUERY_MARGIN_TYPE
        url = f"{Perpetual.BASE_URL}{path}"
        params = {"symbol": symbol}

        try:
            request_data = RequestModel(
                method=HttpMethod.GET,
                login=True,
                url=url,
                params=params,
            )

            response = await self._make_request(request_data)

            return response

        except pydantic_core.ValidationError as e:
            self.logger.debug("Error de Pydantic al crear el RequestModel: %s", str(e))
            raise ApiException(f"Error en Pydantic: {str(e)}") from e

    async def change_margin_type(self, symbol: str, margin_type: str) -> Dict[str, Any]:
        path = Endpoints.CHANGE_MARGIN_TYPE
        url = f"{Perpetual.BASE_URL}{path}"
        params = {"symbol": symbol, "marginType": margin_type}

        try:
            request_data = RequestModel(
                method=HttpMethod.POST,
                login=True,
                url=url,
                params=params,
            )

            response = await self._make_request(request_data)

            return response

        except pydantic_core.ValidationError as e:
            self.logger.debug("Error al crear el RequestModel: %s", str(e))
            raise ApiException(str(e)) from e

    async def _get_sign(self, params_str: str):
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            params_str.encode("utf-8"),
            digestmod=sha256,
        ).hexdigest()
        return signature

    async def _params_str(self, params: Dict[str, Any]) -> str:
        params["timestamp"] = str(self.get_timestamp())
        # Ordenar los parámetros para la firma
        sorted_params = dict(sorted(params.items()))
        params_str = urllib.parse.urlencode(
            sorted_params, safe='{}":,'
        )  # Mantener los caracteres de JSON seguros
        return params_str

    def get_timestamp(self) -> int:
        return int(time.time() * 1_000)

    async def _make_request(
            self, request_data: RequestModel, headers: Optional[Dict[str, Any]] = None
    ) -> aiohttp.http.RESPONSES:
        # Revisar si viene params y data
        params = request_data.params if request_data.params else {}

        # Capturar Headers
        headers = headers if headers else self.headers
        # Pasamos a query string los parámetros
        query_string = await self._params_str(params=params)

        # Creamos la url completa tomando en cuenta si se necesita o no login
        if request_data.login:
            url = f"{request_data.url}?{query_string}&signature={await self._get_sign(query_string)}"
        else:
            url = f"{request_data.url}?{query_string}"

        # hacemos petición
        async with self.session.request(
                request_data.method, url, headers=headers
        ) as response:
            if response.status != 200:
                raise ValueError(
                    f"API Error: {response.status} - {await response.text()}"
                )
            return await response.json()
