import asyncio

from examples.baisc_usage import (
    client_creation,
    get_klines,
)
from src.exceptions.api_exceptions import ApiException
from src.utils.const import Intervals


async def main():
    try:
        client = await client_creation()
        # await server_time_ex(client)
        # await all_contracts_ex(client)
        await get_klines(
            client=client, symbol="BTC-USDT", interval=Intervals.KLINE_4_HOUR
        )

    except ApiException as e:
        print(f"{'*' * 50}")
        print(e)
        print(f"{'*' * 50}")


if __name__ == "__main__":
    asyncio.run(main())
