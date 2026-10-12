from __future__ import annotations

import csv
import io
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import ClassVar


@dataclass(frozen=True)
class Unit:
    code: str
    name: str
    level: str


class AdministrativeCatalog:
    def __init__(self, units: list[Unit], aliases: dict[str, str]):
        self.units = {unit.code: unit for unit in units}
        self.aliases = aliases

    def lookup(self, name_or_code: str) -> Unit | None:
        code = self.aliases.get(name_or_code.lower(), name_or_code)
        return self.units.get(code)


def load_admin_units(payload: dict) -> AdministrativeCatalog:
    units = [Unit(**row) for row in payload["units"]]
    return AdministrativeCatalog(units, {key.lower(): value for key, value in payload.get("aliases", {}).items()})


def load_land_prices(payload: dict) -> list[dict]:
    effective = date.fromisoformat(payload["effective_date"])
    if not payload.get("province_code") or effective.year < 2025:
        raise ValueError("land price table requires a current province and effective date")
    return [{**row, "effective_date": effective.isoformat(), "province_code": payload["province_code"]} for row in payload["rows"]]


def load_sbv_rate(payload: dict) -> dict:
    if not payload.get("published_at") or not payload.get("rate"):
        raise ValueError("SBV fixture requires published_at and rate")
    return payload


class PartnerCsvImporter:
    required: ClassVar[tuple[str, ...]] = ("external_id", "title", "area_m2", "price_vnd")

    def dry_run(self, content: str) -> dict:
        rows = list(csv.DictReader(io.StringIO(content)))
        errors = []
        for index, row in enumerate(rows, start=2):
            row_errors = [f"missing:{field}" for field in sorted(self.required) if not row.get(field)]
            try:
                if float(row.get("area_m2") or "0") <= 0 or int(row.get("price_vnd") or "0") < 0:
                    row_errors.append("invalid_numeric_value")
            except ValueError:
                row_errors.append("invalid_numeric_value")
            if row_errors:
                errors.append({"row": index, "errors": row_errors})
        return {"rows": len(rows), "valid": len(rows) - len(errors), "errors": errors}


class CachedGeocoder:
    def __init__(self, provider: Callable[[str], tuple[float, float]]):
        self.provider = provider
        self.cache: dict[str, tuple[float, float]] = {}

    def geocode(self, address: str) -> tuple[float, float]:
        if address not in self.cache:
            self.cache[address] = self.provider(address)
        return self.cache[address]
