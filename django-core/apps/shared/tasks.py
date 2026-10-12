from __future__ import annotations

from celery import Task, shared_task
from django.utils import timezone

from .models import OutboxEvent
from .reliability import dead_letter


class OutboxTask(Task):
    autoretry_for = (Exception,)
    retry_backoff = True
    retry_backoff_max = 60
    retry_jitter = True
    max_retries = 5

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        dead_letter(self.name, {"args": args, "kwargs": kwargs}, exc, self.max_retries)


@shared_task(bind=True, base=OutboxTask, name="shared.publish_outbox")
def publish_outbox(self, event_id: str) -> None:
    event = OutboxEvent.objects.get(pk=event_id)
    if event.status == "published":
        return
    # Provider dispatch is intentionally an adapter boundary; mark only after it succeeds.
    event.status = "published"
    event.published_at = timezone.now()
    event.attempts += 1
    event.save(update_fields=["status", "published_at", "attempts"])
