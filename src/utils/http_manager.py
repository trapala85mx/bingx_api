"""
Módulo encargado de hacer peticiones HTTP y analizar los Response
y elevar errroes HTTP si corresponde
"""

import logging
from typing import Any, Dict

import aiohttp

from src.exceptions.http_exceptions import HttpException
from src.models.request_model import RequestModel


class HttpManager:

    def __init__(self):
        self.session = None
        self.logger = logging.getLogger(__name__)

    async def make_request(self, request_data: RequestModel) -> Dict[str, Any]:
        """
        Se encarga de hacer la petición.
        Args:
            request_data (RequestModel): Datos para hacer una request.

        Returns:
            Dict[str, Any]: Respuesta del servidor en forma de Diccionario.
        """
        try:
            session = await self._get_session()
            async with session.request(
                    method=request_data.method,
                    url=request_data.url,
                    params=request_data.params,
                    json=request_data.data,
            ) as response:
                await self._verify_response(response)
                if response.status != 200:
                    raise ValueError(
                        f"API Error: {response.status} - {await response.text()}"
                    )
                await self.close()
                return await response.json()

        except HttpException as err:
            print(err)

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Obtiene la sesión para poder realizar peticiones.
        Returns:
            aiohttp.ClientSession: Sesión para poder hacer peticiones.
        """
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _verify_response(
            self, response: aiohttp.ClientResponse
    ) -> aiohttp.ClientResponse:
        """
        Verifica el status code de la respuesta.
        Args:
            response (aiohttp.ClientResponse): Respuesta del Servidor.

        Returns:
            aiohttp.ClientResponse: Respuesta obtenida del Servidor.

        Raises:
            HttpException: Excepción de tipo HTTP derivado de un status code distinto de 2XX.
        """
        status_code = response.status

        if str(status_code).startswith("2"):
            return response

        raise HttpException(
            f"Error en Petición a: {response.url}: Status Code: {status_code}"
        )

    async def close(self) -> None:
        """
        Cierra la sesión del cliente que se encarga de las peticiones.
        Returns:
            None
        """
        if self.session:
            await self.session.close()
