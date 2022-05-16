import json
from typing import Callable, Optional, Sequence, Tuple

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord
from opentelemetry.context.context import Context
from opentelemetry.trace import get_tracer
from opentelemetry.trace.propagation.tracecontext import \
    TraceContextTextMapPropagator

from app.core.configs.kafka_config import kafka_config
from app.core.logs.logging_setup import get_logger

logger = get_logger(__name__)
tracer = get_tracer(__name__)
_config = kafka_config()


def string_deserializer(value: bytes):
    return value.decode("utf-8")


def json_deserializer(value: bytes):
    if not value:
        return None

    return json.loads(value.decode("utf-8"))


async def consume(
        topic: str,
        callback: Callable,
        value_deserializer=json_deserializer,
        auto_offset_reset="earliest"
):
    logger.info(f"Initializing kafka consumer for topic {topic}...")

    consumer = AIOKafkaConsumer(
        topic,
        client_id=_config.client_id,
        group_id=_config.group_id,
        bootstrap_servers=_config.brokers,
        value_deserializer=value_deserializer,
        auto_offset_reset=auto_offset_reset
    )

    await consumer.start()

    logger.info(f"Kafka consumer for topic {topic} initialized!")

    try:
        await _consume(consumer, callback)
    finally:
        logger.info(f"Stopping Kafka consumer for topic {topic}...")

        await consumer.stop()

        logger.info(f"Kafka consumer for topic {topic} stopped!")


async def _consume(consumer: AIOKafkaConsumer, callback: Callable):
    message: ConsumerRecord

    async for message in consumer:
        headers = message.headers
        context: Optional[Context] = _get_context(headers)
        name = f"{message.topic}:{message.partition}:{message.offset}"

        with tracer.start_as_current_span(name, context):
            log = "Consuming {}:{}:{} key={} value={}".format(
                message.topic,
                message.partition,
                message.offset,
                message.key,
                message.value
            )
            logger.info(log)

            await _run_with_dlq(message, callback)


def _get_context(headers: Sequence[Tuple[str, bytes]]) -> Optional[Context]:
    for header in headers:
        if header[0] == 'b3':
            carrier = {"traceparent": header[1].decode("utf-8")}

            return TraceContextTextMapPropagator().extract(carrier=carrier)


async def _run_with_dlq(message: ConsumerRecord, callback: Callable):
    # WIP: Send to DLQ
    await callback(message)
