from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class NotificationProvider(Protocol):
    def send(self, *, event_type: str, payload: dict) -> None: ...


@dataclass
class LoggingNotificationProvider:
    sent: list[tuple[str, dict]]

    def send(self, *, event_type: str, payload: dict) -> None:
        self.sent.append((event_type, payload))


_provider: NotificationProvider = LoggingNotificationProvider([])


def configure_provider(provider: NotificationProvider) -> None:
    global _provider
    _provider = provider


def dispatch_notification(event_type: str, payload: dict) -> None:
    _provider.send(event_type=event_type, payload=payload)
