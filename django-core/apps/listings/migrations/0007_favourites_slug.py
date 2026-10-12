from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [("listings", "0006_postgres_search")]
    operations = [
        migrations.AddField(model_name="listingmodel", name="slug", field=models.SlugField(blank=True, db_index=True, max_length=280)),
        migrations.CreateModel(
            name="FavouriteModel",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("user_id", models.UUIDField(db_index=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("listing", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favourites", to="listings.listingmodel")),
            ],
            options={"db_table": "listing_favourites", "constraints": [models.UniqueConstraint(fields=("user_id", "listing"), name="favourite_user_listing")]},
        ),
    ]
