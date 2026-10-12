from __future__ import annotations

import unicodedata
import xml.etree.ElementTree as ET  # noqa: S405 - DOCTYPE/ENTITY rejected before parsing
from datetime import date

from .fixtures import AdministrativeCatalog, PartnerCsvImporter, Unit, load_land_prices


def fold(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).lower()


def search_units(catalog: AdministrativeCatalog, query: str) -> list[Unit]:
    """Accent- and case-insensitive search over unit names and aliases."""
    needle = fold(query)
    codes = {unit.code for unit in catalog.units.values() if needle in fold(unit.name)}
    codes |= {code for alias, code in catalog.aliases.items() if needle in fold(alias) and code in catalog.units}
    return sorted((catalog.units[code] for code in codes), key=lambda unit: unit.code)


def map_old_unit(catalog: AdministrativeCatalog, payload: dict, old_code: str) -> Unit | None:
    """Map a pre-2025-reform unit code to its post-reform unit using the fixture's old_to_new table."""
    return catalog.units.get(payload.get("old_to_new", {}).get(old_code, ""))


class LandPriceBook:
    """Land price tables versioned by effective date; lookup returns the latest table in force."""

    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add_table(self, payload: dict) -> None:
        self.rows.extend(load_land_prices(payload))

    def lookup(self, commune_code: str, land_use_type: str, on: date) -> dict | None:
        candidates = [
            row
            for row in self.rows
            if row["commune_code"] == commune_code
            and row["land_use_type"] == land_use_type
            and date.fromisoformat(row["effective_date"]) <= on
        ]
        return max(candidates, key=lambda row: row["effective_date"], default=None)


class PartnerXmlImporter:
    """Portal-style XML feed: <listings><listing><external_id/>...</listing></listings>."""

    def parse(self, content: str) -> list[dict]:
        upper = content.upper()
        if "<!DOCTYPE" in upper or "<!ENTITY" in upper:
            raise ValueError("DOCTYPE/ENTITY declarations are not allowed")
        root = ET.fromstring(content)  # noqa: S314
        return [{child.tag: (child.text or "").strip() for child in node} for node in root.findall("listing")]

    def dry_run(self, content: str) -> dict:
        fields = PartnerCsvImporter.required
        lines = [",".join(fields)]
        lines += [",".join(row.get(field, "") for field in fields) for row in self.parse(content)]
        return PartnerCsvImporter().dry_run("\n".join(lines) + "\n")


def csv_template() -> str:
    return ",".join(PartnerCsvImporter.required) + ",description,province_code,commune_code\n"
