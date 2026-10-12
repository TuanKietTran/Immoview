from django.db import migrations, models
from django.db.models import Q
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [("billing", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="PaymentWebhookEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("provider", models.CharField(max_length=30)),
                ("event_id", models.CharField(max_length=200)),
                ("payload_hash", models.CharField(max_length=64)),
                ("processed_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "payment_webhook_events", "constraints": [models.UniqueConstraint(fields=("provider", "event_id"), name="payment_provider_event_unique")]},
        ),
        migrations.CreateModel(
            name="LedgerTransaction",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("reference", models.CharField(max_length=120, unique=True)),
                ("currency", models.CharField(default="VND", max_length=3)),
                ("posted_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "ledger_transactions"},
        ),
        migrations.CreateModel(
            name="LedgerEntry",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("account", models.CharField(max_length=100)),
                ("debit", models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ("credit", models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ("transaction", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="entries", to="billing.ledgertransaction")),
            ],
            options={"db_table": "ledger_entries", "constraints": [models.CheckConstraint(condition=Q(debit__gte=0) & Q(credit__gte=0), name="ledger_nonnegative"), models.CheckConstraint(condition=Q(debit=0) | Q(credit=0), name="ledger_one_side")]},
        ),
    ]
