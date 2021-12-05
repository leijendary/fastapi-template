from asyncio import Lock
from functools import wraps

KEY = '_synchronized_lock'


def synchronized(func):
    lock = Lock()

    setattr(func, KEY, lock)

    @wraps(func)
    async def inner(*args, **kwargs):
        async with lock:
            return await func(*args, **kwargs)

    return inner
