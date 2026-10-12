import uuid
from django.db import models
from apps.leads.domain.entities import LeadStatus, LeadSource


class LeadActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.ForeignKey("LeadModel", on_delete=models.CASCADE, related_name="activities")
    actor_id = models.UUIDField(null=True, blank=True)
    activity_type = models.CharField(max_length=40)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lead_activities"
        ordering = ["created_at"]


class ViewingSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.ForeignKey("LeadModel", on_delete=models.CASCADE, related_name="viewing_slots")
    agent_id = models.UUIDField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    status = models.CharField(max_length=20, default="scheduled")

    def clean(self) -> None:
        from django.core.exceptions import ValidationError
        if self.ends_at <= self.starts_at:
            raise ValidationError({"ends_at": "Viewing slot must end after it starts."})

    class Meta:
        db_table = "lead_viewing_slots"
        constraints = [models.CheckConstraint(condition=models.Q(ends_at__gt=models.F("starts_at")), name="viewing_end_after_start")]


class LeadModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing_id = models.UUIDField(db_index=True)
    agency_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    source = models.CharField(
        max_length=20,
        choices=[(s.value, s.name) for s in LeadSource],
        default=LeadSource.WEBSITE.value,
    )
    status = models.CharField(
        max_length=30,
        choices=[(s.value, s.name) for s in LeadStatus],
        default=LeadStatus.NEW.value,
        db_index=True,
    )
    score = models.SmallIntegerField(null=True, blank=True)  # 0-100 from Lambda scorer
    assigned_agent_id = models.UUIDField(null=True, blank=True, db_index=True)
    sla_due_at = models.DateTimeField(null=True, blank=True, db_index=True)
    sqs_message_id = models.CharField(max_length=100, blank=True)  # for deduplication
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "leads"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["agency_id", "status"]),
            models.Index(fields=["listing_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} → listing {self.listing_id}"
