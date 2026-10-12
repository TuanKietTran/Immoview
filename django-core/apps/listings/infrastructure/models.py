import uuid
from decimal import Decimal
from django.db import models

from apps.listings.domain.entities import ListingStatus, PropertyType, OfferType


class ListingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agency_id = models.UUIDField(db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=[(t.value, t.name) for t in PropertyType])
    offer_type = models.CharField(max_length=10, choices=[(t.value, t.name) for t in OfferType])
    # address
    street = models.CharField(max_length=200)
    street_number = models.CharField(max_length=20)
    postcode = models.CharField(max_length=4)
    city = models.CharField(max_length=100)
    canton = models.CharField(max_length=2)
    # price
    price_chf = models.DecimalField(max_digits=12, decimal_places=2)
    # property details
    area_m2 = models.FloatField()
    rooms = models.FloatField(null=True, blank=True)
    # lifecycle
    status = models.CharField(
        max_length=20,
        choices=[(s.value, s.name) for s in ListingStatus],
        default=ListingStatus.DRAFT.value,
        db_index=True,
    )
    moderation_notes = models.TextField(blank=True)
    fraud_flags = models.JSONField(default=list, blank=True)
    duplicate_key = models.CharField(max_length=128, blank=True, db_index=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "listings"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "offer_type"]),
            models.Index(fields=["postcode"]),
            models.Index(fields=["canton"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.postcode} {self.city})"


class ListingAuditEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(ListingModel, on_delete=models.CASCADE, related_name="audit_events")
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20)
    actor_id = models.UUIDField(null=True, blank=True)
    reason = models.CharField(max_length=500, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "listing_audit_events"
        ordering = ["created_at"]
        indexes = [models.Index(fields=["listing", "created_at"])]


class PhotoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing = models.ForeignKey(ListingModel, on_delete=models.CASCADE, related_name="photos")
    original_key = models.CharField(max_length=500)  # S3 key
    cdn_small = models.CharField(max_length=500, blank=True)
    cdn_medium = models.CharField(max_length=500, blank=True)
    cdn_large = models.CharField(max_length=500, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "listing_photos"
        ordering = ["order"]
