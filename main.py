import asyncio

from examples.baisc_usage import (
    account_data,
    change_margin_type,
    client_creation,
    query_margin_type,
)
from src.exceptions.api_exceptions import ApiException


async def main():
    try:

        client = await client_creation()
        # await server_time_ex(client)
        # await all_contracts_ex(client)
        # await get_klines(
        #    client=client, symbol="BTC-USDT", interval=Intervals.KLINE_4_HOUR
        # )
        await account_data(client=client)
        await query_margin_type(client=client, symbol="BTC-USDT")
        await change_margin_type(
            client=client, symbol="ETH-USDT", margin_type="ISOLATED"
        )
        await client.close()

    except ApiException as e:
        print(f"{'*' * 50}")
        print(e)
        print(f"{'*' * 50}")


if __name__ == "__main__":
    asyncio.run(main())
