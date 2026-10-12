import json
from datetime import date
from pathlib import Path

import pytest

from apps.ingest.connectors import load_admin_units
from apps.ingest.connectors.extras import (
    LandPriceBook,
    PartnerXmlImporter,
    csv_template,
    map_old_unit,
    search_units,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_alias_search_is_accent_insensitive() -> None:
    catalog = load_admin_units(json.loads((FIXTURES / "admin_units_2025.json").read_text()))
    assert [unit.code for unit in search_units(catalog, "da nang")] == ["48"]
    assert [unit.code for unit in search_units(catalog, "hai chau")] == ["48001"]


def test_old_to_new_mapping() -> None:
    payload = {"units": [{"code": "48001", "name": "Hai Chau", "level": "commune"}], "old_to_new": {"old-492": "48001"}}
    catalog = load_admin_units(payload)
    assert map_old_unit(catalog, payload, "old-492").code == "48001"
    assert map_old_unit(catalog, payload, "unknown") is None


def test_land_prices_versioned_by_effective_date() -> None:
    book = LandPriceBook()
    book.add_table(json.loads((FIXTURES / "land_prices_2025.json").read_text()))
    book.add_table(json.loads((FIXTURES / "land_prices_2026.json").read_text()))
    assert book.lookup("48001", "residential", date(2025, 6, 1))["price_vnd_m2"] == 12_000_000
    assert book.lookup("48001", "residential", date(2026, 6, 1))["price_vnd_m2"] == 15_000_000
    assert book.lookup("48001", "residential", date(2024, 1, 1)) is None


def test_xml_dry_run_and_entity_rejection() -> None:
    importer = PartnerXmlImporter()
    result = importer.dry_run((FIXTURES / "partner_feed.xml").read_text())
    assert result["rows"] == 2 and result["valid"] == 1
    assert result["errors"][0]["row"] == 3
    with pytest.raises(ValueError):
        importer.parse('<!DOCTYPE a [<!ENTITY x "y">]><listings/>')


def test_csv_template_has_required_columns() -> None:
    assert csv_template().startswith("external_id,title,area_m2,price_vnd")
