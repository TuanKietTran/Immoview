from apps.shared.notifications import (
    LoggingNotificationProvider,
    configure_provider,
    dispatch_notification,
)


def test_notification_provider_is_replaceable() -> None:
    provider = LoggingNotificationProvider([])
    configure_provider(provider)
    dispatch_notification("lead.created", {"lead_id": "1"})
    assert provider.sent == [("lead.created", {"lead_id": "1"})]
