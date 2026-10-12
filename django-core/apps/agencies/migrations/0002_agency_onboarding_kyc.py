from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [("agencies", "0001_initial")]

    operations = [
        migrations.AddField(model_name="agencymodel", name="status", field=models.CharField(choices=[("onboarding", "Onboarding"), ("pending_approval", "Pending approval"), ("approved", "Approved"), ("suspended", "Suspended")], default="onboarding", max_length=20)),
        migrations.AddField(model_name="agencymodel", name="approved_at", field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name="agencymodel", name="approved_by_id", field=models.UUIDField(blank=True, null=True)),
        migrations.CreateModel(
            name="KycDocument",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("document_type", models.CharField(max_length=50)),
                ("storage_key", models.CharField(max_length=500)),
                ("checksum", models.CharField(max_length=64)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                ("rejected_reason", models.CharField(blank=True, max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("agency", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="kyc_documents", to="agencies.agencymodel")),
            ],
        ),
    ]
