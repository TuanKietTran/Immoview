from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [("listings", "0003_vietnam_fields")]

    operations = [
        migrations.CreateModel(
            name="SavedSearchModel",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("user_id", models.UUIDField(db_index=True)),
                ("name", models.CharField(max_length=120)),
                ("query", models.JSONField(default=dict)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "listing_saved_searches",
                "constraints": [models.UniqueConstraint(fields=("user_id", "name"), name="saved_search_user_name")],
            },
        ),
    ]
