from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("listings", "0004_saved_search")]

    operations = [
        migrations.AddField(model_name="listingmodel", name="latitude", field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
        migrations.AddField(model_name="listingmodel", name="longitude", field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
        migrations.AddField(model_name="listingmodel", name="image_hashes", field=models.JSONField(blank=True, default=list)),
        migrations.AddField(model_name="listingmodel", name="contact_phone", field=models.CharField(blank=True, db_index=True, max_length=30)),
        migrations.AddField(model_name="photomodel", name="image_hash", field=models.CharField(blank=True, db_index=True, max_length=128)),
    ]
