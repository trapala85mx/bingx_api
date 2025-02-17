import asyncio
import gzip
import io
import json
import logging
import uuid
from typing import Optional

import aiohttp

from src.exceptions.stream_exceptions import (
    ChannelException,
    MaxSubscriptionsException,
    StreamException,
)
from src.utils.const import BingxLimits, Endpoints, WsStreamTypes


class WebSocketClient:
    """Clase que representa una conexión WebSocket individual."""

    # Límite de suscripciones por cliente
    max_sub_per_ws: int = BingxLimits.MAX_SUBS_PER_WS.value
    # Límite de conexiones por IP
    max_ws_per_ip: int = BingxLimits.MAX_WS_PER_IP.value

    def __init__(self):
        self.ws_url = Endpoints.WS_URL
        self.subscriptions = {}
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        """Establece la conexión WebSocket."""
        session = aiohttp.ClientSession()
        self.ws = await session.ws_connect(self.ws_url)
        msg = f"Conexión WebSocket establecida con {self.ws_url}"
        self.logger.info(msg)

    async def subscribe(self, channel: str, queue: asyncio.Queue):
        """Suscribe a un canal específico."""
        if len(self.subscriptions) >= WebSocketClient.max_sub_per_ws:
            raise MaxSubscriptionsException(
                "Máximo de suscripciones alcanzado para WebsocketClient"
            )

        subscribe_message = {
            "id": str(uuid.uuid4()),
            "reqType": "sub",
            "dataType": channel,
        }

        await self.ws.send_json(subscribe_message)
        self.subscriptions[channel] = queue

        msg = f"Suscripción al canal {channel} completada."
        self.logger.info(msg)

    async def listen(self) -> None:
        """Escucha mensajes del WebSocket y los redirige a las colas correspondientes."""
        try:
            async for msg in self.ws:

                if msg.type == aiohttp.WSMsgType.TEXT:

                    if msg.data.strip().lower() == "ping":
                        asyncio.create_task(self._send_pong())
                        self.logger.debug("Received Ping, sent Pong")
                        continue

                    data = json.loads(msg.data)
                    channel = data.get("dataType")

                    if not channel:
                        continue

                    if channel in self.subscriptions:
                        await self.subscriptions[channel].put(data)

                if msg.type == aiohttp.WSMsgType.BINARY:

                    decompressed = self._decompress_data(msg.data)

                    if decompressed.strip().lower() == "ping":
                        asyncio.create_task(self._send_pong())
                        self.logger.debug("Received Ping, sent Pong")
                        continue

                    if not decompressed.strip():
                        self.logger.warning(
                            "Received empty decompressed BINARY message"
                        )
                        continue

                    data = json.loads(decompressed)
                    channel = data.get("dataType")

                    if not channel:
                        continue

                    if channel in self.subscriptions:
                        await self.subscriptions[channel].put(data)

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    msg = f"WebSocket error: {msg.data}"
                    self.logger.error(msg)

        except Exception as e:
            msg = f"Error en WebSocket: {e}"
            self.logger.error(msg)
            raise StreamException from e

    async def _send_pong(self):
        try:
            await self.ws.send_str("Pong")
            self.logger.info("Sent Pong in response to Ping")
        except aiohttp.ClientError as e:
            msg = f"Error sending Pong: {e}"
            self.logger.error(msg, exc_info=True)
            raise StreamException(f"Error sending Pong: {e}") from e
        except Exception as e:
            msg = f"Unexpected error sending Pong: {e}"
            self.logger.error(msg, exc_info=True)
            raise StreamException(f"Unexpected error sending Pong: {e}") from e

    def _decompress_data(self, data: bytes) -> str:
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as f:
                decompressed = f.read()
            return decompressed.decode("utf-8")

        except Exception as e:
            msg = f"Error decompressing data: {e}"
            self.logger.error(msg, exc_info=True)
            raise StreamException(f"Error decompressing data: {e}") from e

    def has_capacity(self) -> bool:
        """Indica si el cliente tiene capacidad para más suscripciones."""
        return len(self.subscriptions) < WebSocketClient.max_sub_per_ws

    @staticmethod
    def build_channel_name(channel_type: str, **kwargs) -> str:
        """Construye el nombre del canal a suscribirse."""
        channel = None
        # Suscripción a canal de Klines
        if channel_type.upper() == WsStreamTypes.KLINES_STREAM:
            symbol = kwargs.get("symbol", None)
            interval = kwargs.get("interval", None)

            if (not symbol) or (not interval):
                channel = None
            else:
                channel = f"{symbol}@kline_{interval}"

        if channel is None:
            if channel_type.upper() in [WsStreamTypes.KLINES_STREAM]:
                raise ChannelException(
                    f"Faltaron datos para crear el canal de tipo: {channel_type}"
                )
            raise NotImplementedError(
                f"Aún no se implementa stream para {channel_type}"
            )

        return channel
