"""
DogStatsD client — raw UDP, no external dependency.
All calls are fire-and-forget and silent when the agent is not running.
In production: set DD_DOGSTATSD_HOST env var (default: datadog-agent).
"""
import logging
import socket
from decouple import config

logger = logging.getLogger(__name__)

_sock: socket.socket | None = None
_host: str | None = None
_port = 8125


def _send(payload: str) -> None:
    global _sock, _host
    try:
        if _host is None:
            _host = config("DD_DOGSTATSD_HOST", default="datadog-agent")
        if _sock is None:
            _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _sock.sendto(payload.encode(), (_host, _port))
    except Exception:
        pass  # agent absent — drop silently


def _tag_str(tags: list[str] | None) -> str:
    if not tags:
        return ""
    return "|#" + ",".join(tags)


def increment(metric: str, value: int = 1, tags: list[str] | None = None) -> None:
    _send(f"{metric}:{value}|c{_tag_str(tags)}")


def gauge(metric: str, value: float, tags: list[str] | None = None) -> None:
    _send(f"{metric}:{value}|g{_tag_str(tags)}")


def histogram(metric: str, value: float, tags: list[str] | None = None) -> None:
    _send(f"{metric}:{value}|h{_tag_str(tags)}")


def timing(metric: str, ms: float, tags: list[str] | None = None) -> None:
    _send(f"{metric}:{ms}|ms{_tag_str(tags)}")
