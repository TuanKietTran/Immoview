from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [("shared", "0002_alter_user_groups_alter_user_is_active_and_more")]

    operations = [
        migrations.CreateModel(
            name="OutboxEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("event_type", models.CharField(max_length=120)),
                ("aggregate_type", models.CharField(max_length=80)),
                ("aggregate_id", models.CharField(max_length=100)),
                ("payload", models.JSONField(default=dict)),
                ("status", models.CharField(default="pending", max_length=20)),
                ("attempts", models.PositiveSmallIntegerField(default=0)),
                ("available_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "outbox_events", "indexes": [models.Index(fields=["status", "available_at"], name="outbox_even_status_2b0e75_idx")]},
        ),
        migrations.CreateModel(
            name="IdempotencyRecord",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=255)),
                ("endpoint", models.CharField(max_length=255)),
                ("request_hash", models.CharField(max_length=64)),
                ("response_code", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("response_body", models.JSONField(blank=True, null=True)),
                ("expires_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "idempotency_records", "constraints": [models.UniqueConstraint(fields=("key", "endpoint"), name="idempotency_key_endpoint")]},
        ),
        migrations.CreateModel(
            name="DeadLetterTask",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("task_name", models.CharField(max_length=200)),
                ("payload", models.JSONField(default=dict)),
                ("error", models.TextField()),
                ("attempts", models.PositiveSmallIntegerField(default=0)),
                ("status", models.CharField(default="pending", max_length=20)),
                ("last_attempt_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "dead_letter_tasks", "indexes": [models.Index(fields=["status", "created_at"], name="dead_letter_status_2f4f1b_idx")]},
        ),
    ]
