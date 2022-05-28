import json

from opentelemetry.trace import get_tracer, SpanKind
from opentelemetry.trace.propagation.tracecontext import \
    TraceContextTextMapPropagator
from starlette.types import Message
from starlette.websockets import WebSocket

from app.core.cache.redis_setup import redis, KEY_PAYLOAD
from app.core.logs.logging_setup import get_logger
from app.core.monitoring.tracing import header_trace_parent, header_trace_key

_kind = SpanKind.INTERNAL
logger = get_logger(__name__)
tracer = get_tracer(__name__)


async def redis_subscribe(websocket: WebSocket, key: str, timeout=1.0):
    await websocket.accept()

    pubsub = redis().pubsub()
    await pubsub.subscribe(key)
    name = f"Websocket to {key}"

    try:
        while True:
            message = await pubsub.get_message(True, timeout)

            if message:
                await _send_data(websocket, name, key, message)
    except RuntimeError:
        await websocket.close()
        await pubsub.close()


async def _send_data(
        websocket: WebSocket,
        name: str,
        key: str,
        message: Message
):
    data = json.loads(message["data"])
    trace_header = data[header_trace_key]
    value = data[KEY_PAYLOAD]
    carrier = {header_trace_parent: trace_header}
    context = TraceContextTextMapPropagator().extract(carrier=carrier)

    with tracer.start_as_current_span(name=name, context=context, kind=_kind):
        await websocket.send_json(value)

        logger.info(f"Sent to websocket key={key} data={value}")
