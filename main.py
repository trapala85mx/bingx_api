import asyncio

from examples.baisc_usage import client_creation


async def main():
    client = await client_creation()
    # print(f"Cliente creado en: {client}")
    server_timestamp = await client.server_timestamp()
    print(f"Timestamp del servidor: {server_timestamp}")


if __name__ == "__main__":
    asyncio.run(main())
