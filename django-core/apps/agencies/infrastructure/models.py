import uuid
from django.db import models
from apps.agencies.domain.entities import SubscriptionTier


class AgencyStatus(models.TextChoices):
    ONBOARDING = "onboarding", "Onboarding"
    PENDING_APPROVAL = "pending_approval", "Pending approval"
    APPROVED = "approved", "Approved"
    SUSPENDED = "suspended", "Suspended"


class AgencyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30)
    canton = models.CharField(max_length=2)
    subscription_tier = models.CharField(
        max_length=20,
        choices=[(t.value, t.name) for t in SubscriptionTier],
        default=SubscriptionTier.FREE.value,
    )
    status = models.CharField(max_length=20, choices=AgencyStatus.choices, default=AgencyStatus.ONBOARDING)
    is_active = models.BooleanField(default=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by_id = models.UUIDField(null=True, blank=True)
    seat_limit = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "agencies"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.canton})"


class KycDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agency = models.ForeignKey(AgencyModel, on_delete=models.CASCADE, related_name="kyc_documents")
    document_type = models.CharField(max_length=50)
    storage_key = models.CharField(max_length=500)
    checksum = models.CharField(max_length=64)
    verified_at = models.DateTimeField(null=True, blank=True)
    rejected_reason = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
