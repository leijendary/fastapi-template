import json

from starlette.websockets import WebSocket

from app.core.cache.redis_setup import redis


async def redis_subscribe(websocket: WebSocket, key: str, timeout=1.0):
    await websocket.accept()

    pubsub = redis().pubsub()
    await pubsub.subscribe(key)

    while True:
        message = await pubsub.get_message(True, timeout)

        if message:
            data = json.loads(message["data"])

            await websocket.send_json(data)
