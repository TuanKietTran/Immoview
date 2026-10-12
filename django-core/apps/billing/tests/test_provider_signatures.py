import pytest

from apps.billing.domain.provider_signatures import (
    canonical_for_provider,
    sign_provider_payload,
)
from apps.billing.domain.webhooks import verify_signature

SECRET = "fixture-secret"


@pytest.mark.parametrize(
    ("provider", "payload"),
    [
        ("vnpay", {"vnp_Amount": "100000", "vnp_TxnRef": "INV-1", "vnp_OrderInfo": "Thanh toan", "vnp_SecureHash": "ignored"}),
        ("momo", {"accessKey": "ak", "amount": "100000", "extraData": "", "ipnUrl": "https://example.test/ipn", "orderId": "INV-1", "orderInfo": "Thanh toan", "partnerCode": "MOMO", "redirectUrl": "https://example.test/return", "requestId": "REQ-1", "requestType": "captureWallet"}),
        ("zalopay", {"app_id": 1, "app_trans_id": "240101_INV-1", "app_user": "agency-1", "amount": 100000, "app_time": 1704067200, "embed_data": "{}", "item": "[]"}),
        ("vietqr", {"bank_bin": "970415", "account_no": "123456", "amount": 100000, "reference": "INV-1"}),
        ("stripe", {"t": "1704067200", "body": '{"id":"evt_1","type":"payment_intent.succeeded"}'}),
    ],
)
def test_provider_signature_fixtures(provider: str, payload: dict) -> None:
    base = canonical_for_provider(provider, payload)
    assert base
    signature = sign_provider_payload(provider, payload, SECRET)
    assert verify_signature(provider, payload, signature, SECRET)
    assert not verify_signature(provider, payload, "bad", SECRET)
