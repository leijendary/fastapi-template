import json
from typing import Any, Dict, Type
from typing import Callable, Optional, Sequence, Tuple

from aiokafka import AIOKafkaConsumer
from aiokafka.producer.producer import AIOKafkaProducer
from aiokafka.structs import ConsumerRecord
from opentelemetry.context.context import Context
from opentelemetry.trace import get_tracer, SpanKind
from opentelemetry.trace.propagation.tracecontext import \
    TraceContextTextMapPropagator

from app.core.configs.kafka_config import kafka_config
from app.core.constants import UTF_8
from app.core.logs.logging_setup import get_logger
from app.core.monitoring.tracing import single_span, header_trace_key, \
    header_trace_parent

_config = kafka_config()
logger = get_logger(__name__)
tracer = get_tracer(__name__)


class KafkaProducer:
    instance: AIOKafkaProducer
    span_kind = SpanKind.PRODUCER

    @classmethod
    async def init(cls):
        cls.instance = AIOKafkaProducer(
            client_id=_config.client_id,
            bootstrap_servers=_config.brokers,
            enable_idempotence=True,
            key_serializer=byte_serializer,
            value_serializer=json_serializer
        )
        await cls.instance.start()

    @classmethod
    async def send(
            cls,
            topic: str,
            value: Dict,
            key: str = None,
            partition: int = None
    ):
        span = single_span()
        headers = [(header_trace_key, span.encode(UTF_8))]
        name = f"Produce {topic}:{partition}"

        with tracer.start_span(name=name, kind=cls.span_kind):
            await cls.instance.send(
                topic,
                value,
                key,
                partition,
                headers=headers
            )

        logger.info(f"Sent to topic {topic} key={key} value={value}")


def producer() -> Type[KafkaProducer]:
    return KafkaProducer


async def init():
    logger.info("Starting kafka producer...")

    await KafkaProducer.init()

    logger.info("Kafka producer started!")


async def close():
    logger.info("Stopping kafka producer...")

    await KafkaProducer.instance.stop()

    logger.info("Kafka producer stopped!")


async def health():
    try:
        version = await KafkaProducer.instance.client.check_version()

        return "UP" if version else "DOWN"
    except:
        return "DOWN"


def byte_serializer(value: str):
    if not value:
        return None

    return value.encode(UTF_8)


def json_serializer(value: Any):
    if not value:
        return None

    return json.dumps(value).encode(UTF_8)


def string_deserializer(value: bytes):
    if not value:
        return None

    return value.decode(UTF_8)


def json_deserializer(value: bytes):
    if not value:
        return None

    return json.loads(value.decode(UTF_8))


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
        key_deserializer=string_deserializer,
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
    span_kind = SpanKind.CONSUMER

    async for message in consumer:
        headers = message.headers
        context = _get_context(headers)
        name = f"Consume {message.topic}:{message.partition}:{message.offset}"

        with tracer.start_as_current_span(name, context, kind=span_kind):
            topic = message.topic
            partition = message.partition
            offset = message.offset
            key = message.key
            value = message.value

            logger.info(
                f"Consuming {topic}:{partition}:{offset} key={key} "
                f"value={value}"
            )

            await _run_with_dlq(message, callback)


def _get_context(headers: Sequence[Tuple[str, bytes]]) -> Optional[Context]:
    for header in headers:
        if header[0] == header_trace_key:
            carrier = {
                header_trace_parent: header[1].decode(UTF_8)
            }

            return TraceContextTextMapPropagator().extract(carrier=carrier)


async def _run_with_dlq(message: ConsumerRecord, callback: Callable):
    try:
        await callback(message)
    except Exception:
        topic = message.topic
        value = message.value
        key = message.key
        dlq_topic = f"{topic}.error"

        logger.exception(
            f"Error in consumer for topic {topic}, sending to DLQ {dlq_topic}"
        )

        await KafkaProducer.send(dlq_topic, value, key)
