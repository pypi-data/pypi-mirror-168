import json
import logging
import os
import re
import sys
from functools import partial

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from .middleware import (
    cloud_trace_context,
    http_request_context,
    http_request_middleware_func,
)
from .tracer import add_traces_to_fastapi

GCP_LABELS_LOG_KEY = "logging.googleapis.com/labels"


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def stackdriver_sink(message, project):
    """
    Uses google's structured logging to get nice logs in stackdriver.
    https://cloud.google.com/logging/docs/structured-logging for more info.
    This guide has also server as inspiration
    https://dev.to/floflock/enable-feature-rich-logging-for-fastapi-on-google-cloud-logging-j3i
    """
    record = message.record
    http_request = http_request_context.get()
    labels: dict[str, str] = record.get("extra").get("labels", {})
    log_info = {
        "severity": record["level"].name,
        "message": record["message"],
        "timestamp": record["time"].timestamp(),
        "logging.googleapis.com/sourceLocation": {
            "file": record["file"].name,
            "function": record["function"],
            "line": record["line"],
        },
        GCP_LABELS_LOG_KEY: {
            "x-request-id": correlation_id.get(),
            **labels,
        },
    }
    if http_request is not None:
        log_info["httpRequest"] = http_request

    trace = cloud_trace_context.get()
    if trace is not None:
        split_header = trace.split("/", 1)

        trace_id = f"projects/{project}/traces/{split_header[0]}"

        header_suffix = split_header[1]
        span_id = re.findall(r"^\w+", header_suffix)[0]

        log_info[
            "logging.googleapis.com/trace"
        ] = f"projects/databutton/traces/{trace_id}"
        log_info["spanId"] = span_id
    serialized = json.dumps(log_info)
    print(serialized, file=sys.stderr)


DEFAULT_ZIPKIN_ENDPOINT = os.environ.get(
    "ZIPKIN_ENDPOINT",
    "http://zipkin-gcp.observability.svc.cluster.local:9411/api/v2/spans",
)


def setup_logging_fastapi_gcp(
    app: FastAPI, *, zipkin_endpoint=DEFAULT_ZIPKIN_ENDPOINT, GCP_PROJECT="databutton"
):
    """
    Sets up logging and tracing for FastAPI based projects.
    """
    app.add_middleware(BaseHTTPMiddleware, dispatch=http_request_middleware_func)
    app.add_middleware(CorrelationIdMiddleware)
    if zipkin_endpoint is not None:
        add_traces_to_fastapi(app, zipkin_endpoint=zipkin_endpoint)

    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    logger.remove()
    sink_for_project = partial(stackdriver_sink, project=GCP_PROJECT)
    logger.add(
        sink_for_project,
        # serialize=True,
        level=os.environ.get("LOGURU_LEVEL", "INFO"),
    )
