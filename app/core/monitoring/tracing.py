from typing import Optional

from opentelemetry import trace
from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import format_trace_id, format_span_id, SpanContext
from opentelemetry.trace import get_current_span

from app.core.configs.app_config import app_config
from app.core.configs.monitoring_config import monitoring_config

_app_config = app_config()
_monitoring_config = monitoring_config()


def init():
    endpoint = f"{_monitoring_config.host}:{_monitoring_config.port}"
    jaeger_exporter = JaegerExporter(
        collector_endpoint=endpoint,
        insecure=True
    )
    processor = BatchSpanProcessor(jaeger_exporter)
    resource = Resource.create({
        SERVICE_NAME: _app_config.name
    })
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    set_global_textmap(B3MultiFormat())


def span_context() -> SpanContext:
    return get_current_span().get_span_context()


def get_trace_id() -> Optional[str]:
    context = span_context()
    trace_id = context.trace_id

    if not trace_id:
        return None

    return format_trace_id(trace_id)


def get_span_id() -> Optional[str]:
    context = span_context()
    span_id = context.span_id

    if not span_id:
        return None

    return format_span_id(span_id)


def single_span() -> str:
    context = span_context()
    trace_id = get_trace_id()
    span_id = get_span_id()
    sampled = "01" if context.trace_flags.sampled else "00"

    return f"00-{trace_id}-{span_id}-{sampled}"
