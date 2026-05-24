import uuid
from django.db import models


class ValuationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing_id = models.UUIDField(null=True, blank=True, db_index=True)
    agency_id = models.UUIDField(null=True, blank=True)
    canton = models.CharField(max_length=2)
    property_type = models.CharField(max_length=20)
    offer_type = models.CharField(max_length=10)
    area_m2 = models.FloatField()
    rooms = models.FloatField(null=True, blank=True)
    estimate_chf = models.DecimalField(max_digits=14, decimal_places=2)
    range_low_chf = models.DecimalField(max_digits=14, decimal_places=2)
    range_high_chf = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "valuations"
        ordering = ["-created_at"]
