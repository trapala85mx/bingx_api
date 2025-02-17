from decouple import config

from src.api.client import Perpetual


async def client_creation() -> Perpetual:
    api_key = config("BINGX_API_KEY")
    api_secret = config("BINGX_API_SECRET")
    client = Perpetual(api_key=api_key, secret=api_secret)
    return client


async def server_time_ex(client: Perpetual):
    server_timestamp = await client.server_timestamp()
    print(f"Timestamp del servidor:\n {server_timestamp}")


async def all_contracts_ex(client: Perpetual):
    contracts_data = await client.contracts()
    print("Data de contratos:\n", contracts_data)


async def get_klines(client: Perpetual, symbol: str, interval: str):
    klines_data = await client.kline_data(symbol=symbol, interval=interval)
    print("Data de Klines:\n", klines_data)


async def account_data(client: Perpetual):
    acc_data = await client.account_data()
    print("Data de cuenta:\n", acc_data)


async def query_margin_type(client: Perpetual, symbol: str):
    mar_ty = await client.query_margin_type(symbol=symbol)
    print(f"Margin type para {symbol}:\n {mar_ty}")


async def change_margin_type(client: Perpetual, symbol: str, margin_type: str):
    resp = await client.change_margin_type(symbol=symbol, margin_type=margin_type)
    print(f"Modificado el margin type para {symbol}:\n {resp}")
