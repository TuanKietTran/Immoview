import uuid
from django.db import models
from apps.leads.domain.entities import LeadStatus, LeadSource


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
