import asyncio

from examples.baisc_usage import (
    account_data,
    change_margin_type,
    client_creation,
    query_margin_type,
    server_time_ex,
)
from examples.websocket_usage import (
    websocket_usage,
)
from src.api.client import Perpetual
from src.exceptions.api_exceptions import ApiException
from src.utils.const import BingxLimits


async def api_basic_usage(client: Perpetual):
    await server_time_ex(client)
    # await all_contracts_ex(client)
    # await get_klines(client=client, symbol="BTC-USDT", interval=Intervals.KLINE_4_HOUR)
    await account_data(client=client)
    await query_margin_type(client=client, symbol="BTC-USDT")
    await change_margin_type(client=client, symbol="ETH-USDT", margin_type="ISOLATED")


async def main():
    client = None
    try:
        client = await client_creation()
        await websocket_usage(client)

        while True:
            # Tiempo que dura la listen key
            await asyncio.sleep(BingxLimits.LISTEN_KEY_RENEWAL_SECS.value)
            # Renovar listen key
            await client.extend_listen_key()
            print("Listen Key Extendida")

    except ApiException as e:
        print(f"{'*' * 50}")
        print(e)
        print(f"{'*' * 50}")

    except Exception as e:
        print("ERROR INESPERADO")
        # Cerrar clientes de API y/o Websocket
        # client.close()
        # ws_manager.close_all()
        if client:
            await client.delete_listen_key()


if __name__ == "__main__":
    asyncio.run(main())
