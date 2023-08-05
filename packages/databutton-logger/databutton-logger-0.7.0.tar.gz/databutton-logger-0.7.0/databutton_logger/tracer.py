from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def add_traces_to_fastapi(app: FastAPI, *, zipkin_endpoint: str):
    trace.set_tracer_provider(TracerProvider())
    zipkin_exporter = ZipkinExporter(endpoint=zipkin_endpoint)
    span_processor = BatchSpanProcessor(zipkin_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())
