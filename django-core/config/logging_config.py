"""
Datadog-compatible JSON log formatter.
Each record includes dd.trace_id / dd.span_id for log-to-trace correlation.
Format follows Datadog's standard attribute names.
"""
import json
import logging
import time


class DatadogJSONFormatter(logging.Formatter):
    SERVICE = "django-core"

    def format(self, record: logging.LogRecord) -> str:
        entry: dict = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%03dZ"),
            "level": record.levelname,
            "logger.name": record.name,
            "message": record.getMessage(),
            "service": self.SERVICE,
        }

        # Datadog trace correlation — injected when ddtrace is active
        try:
            from ddtrace import tracer
            span = tracer.current_span()
            if span:
                entry["dd.trace_id"] = str(span.trace_id)
                entry["dd.span_id"] = str(span.span_id)
        except Exception:
            pass

        if record.exc_info:
            entry["error.stack"] = self.formatException(record.exc_info)
            entry["error.kind"] = record.exc_info[0].__name__ if record.exc_info[0] else ""

        # Pass-through any extra fields added via `extra={}` in log calls
        _stdlib = frozenset((
            "args", "created", "exc_info", "exc_text", "filename", "funcName",
            "levelname", "levelno", "lineno", "message", "module", "msecs",
            "msg", "name", "pathname", "process", "processName", "relativeCreated",
            "stack_info", "thread", "threadName",
        ))
        for key, val in record.__dict__.items():
            if key not in _stdlib and not key.startswith("_"):
                entry[key] = val

        return json.dumps(entry, default=str)

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        ct = record.created
        t = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(ct))
        return f"{t}.{int(record.msecs):03d}Z"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "config.logging_config.DatadogJSONFormatter",
        },
        "simple": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "stdout_json": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
        "stdout_simple": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "apps": {
            "level": "INFO",
            "propagate": False,
        },
        "config": {
            "level": "INFO",
            "propagate": False,
        },
        # Suppress Django's routine 400/404 noise — real errors still surface
        "django.request": {
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "level": "WARNING",
            "propagate": False,
        },
    },
    "root": {
        "level": "WARNING",
        "handlers": [],  # filled in by settings.py based on DEBUG flag
    },
}
