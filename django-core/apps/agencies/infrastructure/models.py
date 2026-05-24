import uuid
from django.db import models
from apps.agencies.domain.entities import SubscriptionTier


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
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "agencies"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.canton})"
