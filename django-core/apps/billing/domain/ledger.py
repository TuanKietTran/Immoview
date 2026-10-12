from __future__ import annotations

from decimal import Decimal
from django.db import transaction

from apps.billing.infrastructure.models import LedgerEntry, LedgerTransaction


@transaction.atomic
def post_transaction(reference: str, currency: str, entries: list[dict]) -> LedgerTransaction:
    if len(entries) < 2:
        raise ValueError("A ledger transaction needs at least two entries")
    debit = sum((Decimal(str(item.get("debit", 0))) for item in entries), Decimal(0))
    credit = sum((Decimal(str(item.get("credit", 0))) for item in entries), Decimal(0))
    if debit <= 0 or debit != credit:
        raise ValueError("Ledger transaction must balance positive debits and credits")
    tx = LedgerTransaction.objects.create(reference=reference, currency=currency)
    LedgerEntry.objects.bulk_create([
        LedgerEntry(transaction=tx, account=item["account"], debit=item.get("debit", 0), credit=item.get("credit", 0))
        for item in entries
    ])
    return tx
