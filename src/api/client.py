import hmac
import logging
import time
import urllib
from hashlib import sha256
from typing import Any, Dict, Optional

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
        try:
            request_data = RequestModel(
                method=method,
                url=url,
                params=params if params else {},
                data=data if data else {},
                login=signed,
            )

            response = await self.http_manager.make_request(request_data=request_data)
            await self.http_manager.close()
            return response["data"]["serverTime"]

        except pydantic_core.ValidationError as err:
            self.logger.debug("Error al crear el RequestModel: %s", str(err))

    async def contracts(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Arma lo neceasrio para realizar la petición al endpoint para traer la información de los contratos
        Args:
            symbol (Optional[Dict[str,Any]]): Ticker symbol del activo del cual se quiere obtener la info. Default. None

        Returns:
            Dict[str,Any]: Respuesta del Servidor.
        """
        endpoint = Endpoints.CONTRACTS
        method = HttpMethod.GET
        url = f"{Perpetual.BASE_URL}{endpoint}"
        signed = False

        params = None
        data = None

        if symbol:
            if len(symbol) > 0:
                params["symbol"] = symbol
        try:
            request_data = RequestModel(
                method=method,
                url=url,
                params=params if params else {},
                data=data if data else {},
                login=signed,
            )

            response = await self.http_manager.make_request(request_data=request_data)
            await self.http_manager.close()
            return response
        except pydantic_core.ValidationError as err:
            self.logger.debug("Error al crear el RequestModel: %s", str(err))

    async def kline_data(self, symbol: str, interval: str, **kwargs) -> Dict[str, Any]:
        path = Endpoints.KLINES
        method = HttpMethod.GET
        signed = False
        url = f"{Perpetual.BASE_URL}{path}"

        data = None
        params = {"symbol": symbol, "interval": interval}
        start = kwargs.get("start", None)
        end = kwargs.get("end", None)

        if start:
            params["startTime"] = start
        if end:
            params["endTime"] = end

        try:
            request_data = RequestModel(
                method=method,
                url=url,
                params=params if params else {},
                data=data if data else {},
                login=signed,
            )

            response = await self.http_manager.make_request(request_data=request_data)
            await self.http_manager.close()
            return response
        except pydantic_core.ValidationError as err:
            self.logger.debug("Error al crear el RequestModel: %s", str(err))
            raise ApiException(str(err)) from err

    async def account_data(self) -> Dict[str, Any]:
        method = HttpMethod.GET
        path = Endpoints.ACCOUNT
        signed = True
        data = None
        params = None
        url = f"{Perpetual.BASE_URL}{path}"

        params = await self._get_body_data()

        try:
            request_data = RequestModel(
                method=method,
                login=signed,
                url=url,
                params=params if params else {},
                data=data if data else {},
            )

            self.headers.update({"Content-Type": "application/json"})
            response = await self.http_manager.make_request(request_data, self.headers)

            await self.http_manager.close()
            return response

        except pydantic_core.ValidationError as e:
            self.logger.debug("Error al crear el RequestModel: %s", str(e))
            raise ApiException(str(e)) from e

    async def _get_body_data(
            self, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        params = params if params else {}
        params["timestamp"] = str(self.get_timestamp())
        signature = self._get_sign(self._params_str(params))
        params["signature"] = signature
        return params

    def _get_sign(self, params_str: str):
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            params_str.encode("utf-8"),
            digestmod=sha256,
        ).hexdigest()
        return signature

    def get_timestamp(self) -> int:
        return int(time.time() * 1_000)

    def _params_str(self, params: Dict[str, Any]) -> str:
        # Ordenar los parámetros para la firma
        sorted_params = dict(sorted(params.items()))
        params_str = urllib.parse.urlencode(
            sorted_params, safe='{}":,'
        )  # Mantener los caracteres de JSON seguros
        return params_str
