from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("listings", "0007_favourites_slug")]
    operations = [migrations.AddField(model_name="listingmodel", name="source_external_id", field=models.CharField(blank=True, db_index=True, max_length=160, unique=True))]
