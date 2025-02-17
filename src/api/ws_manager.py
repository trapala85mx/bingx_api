import asyncio
import logging
from typing import List

from src.api.ws_client import WebSocketClient
from src.exceptions.stream_exceptions import MaxWebsocketConnectionException


class WebSocketManager:
    """Gestor de conexiones WebSocket."""

    def __init__(self):
        self.clients: List[WebSocketClient] = []
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """Inicializa la primera conexión WebSocket."""
        await self._create_new_client()

    async def subscribe(self, channel_type: str, **kwargs) -> asyncio.Queue:
        """Suscribe a un canal y retorna una cola para recibir mensajes."""
        channel = WebSocketClient.build_channel_name(channel_type, **kwargs)
        queue = asyncio.Queue()

        # Intentar suscribirse en un cliente existente con capacidad
        for client in self.clients:
            if client.has_capacity():
                await client.subscribe(channel, queue)
                return queue

        # Si no hay espacio en los clientes existentes, verificar límite de clientes
        if len(self.clients) >= WebSocketClient.max_ws_per_ip:
            raise MaxWebsocketConnectionException(
                f"Se alcanzó el máximo número de conexiones WebSocket permitidas por IP. No se pudo suscribir al canal: {channel}"
            )

        # Crear un nuevo cliente si aún hay espacio permitido
        client = await self._create_new_client()
        await client.subscribe(channel, queue)
        return queue, channel

    async def close_all(self):
        """Cierra todas las conexiones WebSocket."""
        for client in self.clients:
            await client.ws.close()
        self.logger.info("Todas las conexiones WebSocket han sido cerradas.")

    async def _create_new_client(self) -> WebSocketClient:
        """Crea un nuevo cliente WebSocket y lo inicia."""
        if len(self.clients) >= WebSocketClient.max_ws_per_ip:
            raise ValueError("Máximo de conexiones WebSocket alcanzado.")
        client = WebSocketClient()
        await client.connect()
        asyncio.create_task(client.listen())  # Ejecutar en segundo plano
        self.clients.append(client)
        self.logger.info("Nuevo cliente WebSocket creado.")
        return client
