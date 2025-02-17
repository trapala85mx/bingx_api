import asyncio
from typing import Any, Dict, List

from src.api.ws_manager import WebSocketManager
from src.utils.const import Intervals, WsStreamTypes

queue_map: Dict[str, Any] = {}
tasks: List[asyncio.Task] = []


async def websocket_usage():
    # Este se debe crear en el flujo principal, cada estrategia lo recibe
    ws_manager = WebSocketManager()
    # Cada estrategia se inica para cada symbol
    await staregy_example(ws_manager=ws_manager)


async def staregy_example(ws_manager: WebSocketManager):
    # suscribimos a canal
    que, chann = await kline_subscription(
        channel_type=WsStreamTypes.KLINES_STREAM,
        symbol="BTC-USDT",
        interval=Intervals.KLINE_15_MIN,
        ws_manager=ws_manager,
    )
    # La estrategia debe asociar el canal con su cola
    queue_map[chann] = que
    # Analizar axincronamente cada tarea
    tasks.append(asyncio.create_task(process_queue(chann)))
    # Hasta aqui el flujo continuará pero, en segundo plano se ejecutan estas tareas
    # Por lo que se necesita un ciclo infinito en el main para no terminar las tareas
    # Forzosamente


async def process_queue(channel: str):
    # Aqui analizamos infinitamante la cola, en este caso la única que se tieene,
    # y se analiza lo necesario para la estraegia. Se analiza cada cola con una función
    # o como sea necesario de acuerdo a la estretegia.
    while True:
        # Obtener la info de la cola
        data = await queue_map[channel].get()
        # El mensaje recibido que nos interesa es la que tiene la llave 'data'
        if not data.get("data"):
            continue
        # Lo mismo, ahora sí viene 'data' pero vacío
        if len(data) == 0:
            continue

        # Aqui viene la lógica a usar con la data recibida
        print(data)


async def kline_subscription(
        channel_type: str,
        symbol: str,
        interval: str,
        ws_manager: WebSocketManager,
):
    # Ejemplo de suscripción a klines
    klines_queue = await ws_manager.subscribe(
        channel_type=channel_type, interval=interval, symbol=symbol
    )

    return klines_queue
