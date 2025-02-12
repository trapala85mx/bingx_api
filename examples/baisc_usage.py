from src.api.client import Perpetual


async def client_creation() -> Perpetual:
    client = Perpetual()
    return client
