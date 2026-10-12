import json

from django.test import RequestFactory

from apps.shared.health import liveness


def test_liveness_is_process_only() -> None:
    response = liveness(RequestFactory().get("/health/"))
    assert response.status_code == 200
    assert json.loads(response.content) == {"status": "ok"}
