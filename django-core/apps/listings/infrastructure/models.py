import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator
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
    # Vietnam marketplace fields; legacy Swiss fields remain during migration.
    price_vnd = models.BigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    price_per_m2_vnd = models.BigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    province_code = models.CharField(max_length=10, blank=True, db_index=True)
    commune_code = models.CharField(max_length=10, blank=True, db_index=True)
    legal_status = models.CharField(max_length=40, blank=True)
    direction = models.CharField(max_length=20, blank=True)
    frontage_m = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    alley_width_m = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    floors = models.PositiveSmallIntegerField(null=True, blank=True)
    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    project = models.CharField(max_length=255, blank=True)
    developer = models.CharField(max_length=255, blank=True)
    planning_status = models.CharField(max_length=40, blank=True)
    land_use_type = models.CharField(max_length=40, blank=True)
    # property details
    area_m2 = models.FloatField(validators=[MinValueValidator(0)])
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

    def clean(self) -> None:
        super().clean()
        if self.price_per_m2_vnd is not None and self.price_vnd is None:
            from django.core.exceptions import ValidationError
            raise ValidationError({"price_per_m2_vnd": "A VND listing price is required first."})

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


class SavedSearchModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=120)
    query = models.JSONField(default=dict)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "listing_saved_searches"
        constraints = [models.UniqueConstraint(fields=["user_id", "name"], name="saved_search_user_name")]


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
