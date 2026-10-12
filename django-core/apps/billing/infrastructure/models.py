import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Q


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class InvoiceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agency_id = models.UUIDField(db_index=True)
    amount_chf = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)
    period_start = models.DateField()
    period_end = models.DateField()
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "invoices"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Invoice {self.id} — CHF {self.amount_chf} ({self.status})"


class PaymentWebhookEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=30)
    event_id = models.CharField(max_length=200)
    payload_hash = models.CharField(max_length=64)
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payment_webhook_events"
        constraints = [models.UniqueConstraint(fields=["provider", "event_id"], name="payment_provider_event_unique")]


class LedgerTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=120, unique=True)
    currency = models.CharField(max_length=3, default="VND")
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ledger_transactions"


class LedgerEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(LedgerTransaction, on_delete=models.CASCADE, related_name="entries")
    account = models.CharField(max_length=100)
    debit = models.DecimalField(max_digits=20, decimal_places=0, default=0)
    credit = models.DecimalField(max_digits=20, decimal_places=0, default=0)

    class Meta:
        db_table = "ledger_entries"
        constraints = [
            models.CheckConstraint(condition=Q(debit__gte=0) & Q(credit__gte=0), name="ledger_nonnegative"),
            models.CheckConstraint(condition=(Q(debit=0) | Q(credit=0)), name="ledger_one_side"),
        ]
