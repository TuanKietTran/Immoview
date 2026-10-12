from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="IngestRun",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("source", models.CharField(max_length=100)), ("status", models.CharField(default="running", max_length=20)),
                ("fetched_count", models.PositiveIntegerField(default=0)), ("imported_count", models.PositiveIntegerField(default=0)),
                ("error_count", models.PositiveIntegerField(default=0)), ("started_at", models.DateTimeField(auto_now_add=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)), ("error", models.TextField(blank=True)),
            ], options={"db_table": "ingest_runs", "ordering": ["-started_at"]},
        ),
        migrations.CreateModel(
            name="RawLanding",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("source", models.CharField(max_length=100)), ("external_id", models.CharField(max_length=200)),
                ("payload", models.JSONField()), ("payload_hash", models.CharField(max_length=64)),
                ("fetched_at", models.DateTimeField(auto_now_add=True)), ("content_type", models.CharField(default="application/json", max_length=100)),
                ("replayed_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={"db_table": "ingest_raw_landing", "indexes": [models.Index(fields=["source", "fetched_at"], name="ingest_raw_source_8be28a_idx")], "constraints": [models.UniqueConstraint(fields=("source", "external_id", "payload_hash"), name="raw_source_external_hash")]},
        ),
        migrations.CreateModel(
            name="IngestDeadLetter",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("source", models.CharField(max_length=100)), ("external_id", models.CharField(max_length=200)),
                ("payload", models.JSONField()), ("error", models.TextField()), ("attempts", models.PositiveSmallIntegerField(default=0)),
                ("status", models.CharField(default="pending", max_length=20)), ("created_at", models.DateTimeField(auto_now_add=True)),
                ("run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="dead_letters", to="ingest.ingestrun")),
            ], options={"db_table": "ingest_dead_letters", "indexes": [models.Index(fields=["source", "status"], name="ingest_dead_source_6cd29e_idx")]},
        ),
    ]
