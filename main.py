import asyncio

from examples.baisc_usage import client_creation
from src.api.client import Perpetual


async def server_time_ex(client: Perpetual):
    server_timestamp = await client.server_timestamp()
    print(f"Timestamp del servidor: {server_timestamp}")


async def all_contracts_ex(client: Perpetual):
    contracts_data = await client.contracts()
    print(contracts_data)


async def main():
    client = await client_creation()
    # await server_time_ex(client)
    await all_contracts_ex(client)


if __name__ == "__main__":
    asyncio.run(main())
