from decouple import config

from src.api.client import Perpetual


async def client_creation() -> Perpetual:
    api_key = config("BINGX_API_KEY")
    api_secret = config("BINGX_API_SECRET")
    client = Perpetual(api_key=api_key, secret=api_secret)
    return client


async def server_time_ex(client: Perpetual):
    server_timestamp = await client.server_timestamp()
    print(f"Timestamp del servidor: {server_timestamp}")


async def all_contracts_ex(client: Perpetual):
    contracts_data = await client.contracts()
    print(contracts_data)


async def get_klines(client: Perpetual, symbol: str, interval: str):
    klines_data = await client.kline_data(symbol=symbol, interval=interval)
    print(klines_data)


async def account_data(client: Perpetual):
    acc_data = await client.account_data()
    print(acc_data)
