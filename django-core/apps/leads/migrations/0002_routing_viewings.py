from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [("leads", "0001_initial")]

    operations = [
        migrations.AddField(model_name="leadmodel", name="assigned_agent_id", field=models.UUIDField(blank=True, db_index=True, null=True)),
        migrations.AddField(model_name="leadmodel", name="sla_due_at", field=models.DateTimeField(blank=True, db_index=True, null=True)),
        migrations.CreateModel(
            name="LeadActivity",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("actor_id", models.UUIDField(blank=True, null=True)),
                ("activity_type", models.CharField(max_length=40)),
                ("note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("lead", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="activities", to="leads.leadmodel")),
            ],
            options={"db_table": "lead_activities", "ordering": ["created_at"]},
        ),
        migrations.CreateModel(
            name="ViewingSlot",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("agent_id", models.UUIDField()),
                ("starts_at", models.DateTimeField()),
                ("ends_at", models.DateTimeField()),
                ("status", models.CharField(default="scheduled", max_length=20)),
                ("lead", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="viewing_slots", to="leads.leadmodel")),
            ],
            options={"db_table": "lead_viewing_slots", "constraints": [models.CheckConstraint(condition=models.Q(ends_at__gt=models.F("starts_at")), name="viewing_end_after_start")]},
        ),
    ]
