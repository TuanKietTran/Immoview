from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("listings", "0008_external_key")]
    operations = [migrations.AlterField(model_name="listingmodel", name="source_external_id", field=models.CharField(blank=True, db_index=True, default=None, max_length=160, null=True, unique=True))]
