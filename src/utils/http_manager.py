"""
Módulo encargado de hacer peticiones HTTP y analizar los Response
y elevar errroes HTTP si corresponde
"""

import logging
from typing import Any, Dict

import aiohttp

from src.exceptions.http_exceptions import HttpException


class HttpManager:

    def __init__(self):
        self.session = None
        self.logger = logging.getLogger(__name__)

    async def make_request(
            self,
            method: str,
            url: str,
            headers: Dict[str, Any],
    ) -> aiohttp.http.RESPONSES:
        """
        Realiza una petición HTTP.
        Args:
            method (str): Tipo de petición HTTP para la petición.
            url (str): URL final siguiendo instrucciones para envío de data mediante query string.
            headers (Dict[str,Any]]): Headers para la petición.

        Returns:
            Dict[str,Any]: Response de la petición den formato de Diccionario.

        Raises:
            HttpException: Error de tipo HTTP indicando una respuesta no exitosa.
        """
        session = await self._get_session()

        # hacemos petición
        async with session.request(method=method, url=url, headers=headers) as response:
            if not str(response.status).startswith("2"):
                raise HttpException(
                    f"HTTP Error: {response.status} - {await response.text()}"
                )
            return await response.json()

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Retorna una sesión.

        Returns:
            aiohttp.ClientSession: Sessión para hacer peticiones.
        """
        if not self.session:
            self.session = aiohttp.ClientSession()

        return self.session

    async def close(self) -> None:
        """
        Cierra la sesión del cliente que se encarga de las peticiones.
        Returns:
            None
        """
        if self.session:
            await self.session.close()
