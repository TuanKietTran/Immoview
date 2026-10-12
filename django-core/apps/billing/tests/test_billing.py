from decimal import Decimal

import pytest

from apps.billing.domain.ledger import post_transaction
from apps.billing.domain.webhooks import canonical_payload, claim_webhook


def test_webhook_signature_and_replay_protection(db: None) -> None:
    payload = {"amount": 100, "currency": "VND"}
    import hmac
    import hashlib
    signature = hmac.new(b"secret", canonical_payload(payload), hashlib.sha256).hexdigest()
    assert claim_webhook("vnpay", "event-1", payload, signature, "secret") is True
    assert claim_webhook("vnpay", "event-1", payload, signature, "secret") is False
    with pytest.raises(ValueError):
        claim_webhook("vnpay", "event-2", payload, "bad", "secret")


@pytest.mark.django_db
def test_double_entry_transaction_balances(db: None) -> None:
    tx = post_transaction("payment-1", "VND", [
        {"account": "cash", "debit": 1000},
        {"account": "wallet", "credit": 1000},
    ])
    assert sum(entry.debit for entry in tx.entries.all()) == Decimal("1000")
    with pytest.raises(ValueError):
        post_transaction("payment-2", "VND", [{"account": "cash", "debit": 1000}, {"account": "wallet", "credit": 900}])
