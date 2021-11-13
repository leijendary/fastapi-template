from httpx import AsyncClient

client = AsyncClient()


async def close():
    await client.aclose()
