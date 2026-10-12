import pytest
from django.test import RequestFactory

from apps.listings.sitemap import sitemap


@pytest.mark.django_db
def test_sitemap_is_xml() -> None:
    response = sitemap(RequestFactory().get("/sitemap.xml"))
    assert response.status_code == 200
    assert response["Content-Type"] == "application/xml"
    assert b"urlset" in response.content
