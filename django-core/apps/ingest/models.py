import uuid

from django.db import models


class IngestRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="running")
    fetched_count = models.PositiveIntegerField(default=0)
    imported_count = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True)

    class Meta:
        db_table = "ingest_runs"
        ordering = ["-started_at"]


class RawLanding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=100)
    external_id = models.CharField(max_length=200)
    payload = models.JSONField()
    payload_hash = models.CharField(max_length=64)
    fetched_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=100, default="application/json")
    replayed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "ingest_raw_landing"
        constraints = [models.UniqueConstraint(fields=["source", "external_id", "payload_hash"], name="raw_source_external_hash")]
        indexes = [models.Index(fields=["source", "fetched_at"])]

    def delete(self, *args, **kwargs):
        raise ValueError("Raw landing is immutable and cannot be deleted")


class IngestDeadLetter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    run = models.ForeignKey(IngestRun, on_delete=models.CASCADE, related_name="dead_letters")
    source = models.CharField(max_length=100)
    external_id = models.CharField(max_length=200)
    payload = models.JSONField()
    error = models.TextField()
    attempts = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ingest_dead_letters"
        indexes = [models.Index(fields=["source", "status"])]
