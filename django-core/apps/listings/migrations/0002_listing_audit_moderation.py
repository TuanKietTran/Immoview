from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [("listings", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="listingmodel",
            name="moderation_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="listingmodel",
            name="fraud_flags",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="listingmodel",
            name="duplicate_key",
            field=models.CharField(blank=True, db_index=True, max_length=128),
        ),
        migrations.CreateModel(
            name="ListingAuditEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("from_status", models.CharField(blank=True, max_length=20)),
                ("to_status", models.CharField(max_length=20)),
                ("actor_id", models.UUIDField(blank=True, null=True)),
                ("reason", models.CharField(blank=True, max_length=500)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("listing", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="audit_events", to="listings.listingmodel")),
            ],
            options={
                "db_table": "listing_audit_events",
                "ordering": ["created_at"],
                "indexes": [models.Index(fields=["listing", "created_at"], name="listing_aud_listing_1f1b3d_idx")],
            },
        ),
    ]
