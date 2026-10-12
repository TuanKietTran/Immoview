import json
from pathlib import Path

from apps.ingest.connectors import (
    CachedGeocoder,
    PartnerCsvImporter,
    load_admin_units,
    load_land_prices,
    load_sbv_rate,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_admin_alias_and_land_price_contract_fixtures() -> None:
    catalog = load_admin_units(json.loads((FIXTURES / "admin_units_2025.json").read_text()))
    assert catalog.lookup("Đà Nẵng").code == "48"
    assert catalog.lookup("old-hai-chau-district").code == "48001"
    assert load_land_prices(json.loads((FIXTURES / "land_prices_2026.json").read_text()))[0]["price_vnd_m2"] == 15_000_000
    assert load_sbv_rate(json.loads((FIXTURES / "sbv_rate.json").read_text()))["rate"] == 25300


def test_partner_csv_dry_run_reports_errors() -> None:
    result = PartnerCsvImporter().dry_run("external_id,title,area_m2,price_vnd\na-1,Home,50,1000\na-2,,0,bad\n")
    assert result == {"rows": 2, "valid": 1, "errors": [{"row": 3, "errors": ["missing:title", "invalid_numeric_value"]}]}


def test_geocoder_is_cached() -> None:
    calls = []
    geocoder = CachedGeocoder(lambda address: (calls.append(address) or (16.0, 108.0)))
    assert geocoder.geocode("A") == geocoder.geocode("A")
    assert calls == ["A"]
