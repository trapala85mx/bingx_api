from src.api.client import Perpetual


async def client_creation() -> Perpetual:
    client = Perpetual()
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
