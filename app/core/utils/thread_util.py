from asyncio import Lock
from functools import wraps


def synchronized(func):
    lock = Lock()

    @wraps(func)
    async def inner(*args, **kwargs):
        async with lock:
            return await func(*args, **kwargs)

    return inner
