from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("listings", "0002_listing_audit_moderation")]

    operations = [
        migrations.AddField(model_name="listingmodel", name="price_vnd", field=models.BigIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])),
        migrations.AddField(model_name="listingmodel", name="price_per_m2_vnd", field=models.BigIntegerField(blank=True, null=True, validators=[MinValueValidator(0)])),
        migrations.AddField(model_name="listingmodel", name="province_code", field=models.CharField(blank=True, db_index=True, max_length=10)),
        migrations.AddField(model_name="listingmodel", name="commune_code", field=models.CharField(blank=True, db_index=True, max_length=10)),
        migrations.AddField(model_name="listingmodel", name="legal_status", field=models.CharField(blank=True, max_length=40)),
        migrations.AddField(model_name="listingmodel", name="direction", field=models.CharField(blank=True, max_length=20)),
        migrations.AddField(model_name="listingmodel", name="frontage_m", field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[MinValueValidator(0)])),
        migrations.AddField(model_name="listingmodel", name="alley_width_m", field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, validators=[MinValueValidator(0)])),
        migrations.AddField(model_name="listingmodel", name="floors", field=models.PositiveSmallIntegerField(blank=True, null=True)),
        migrations.AddField(model_name="listingmodel", name="bedrooms", field=models.PositiveSmallIntegerField(blank=True, null=True)),
        migrations.AddField(model_name="listingmodel", name="project", field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name="listingmodel", name="developer", field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name="listingmodel", name="planning_status", field=models.CharField(blank=True, max_length=40)),
        migrations.AddField(model_name="listingmodel", name="land_use_type", field=models.CharField(blank=True, max_length=40)),
    ]
