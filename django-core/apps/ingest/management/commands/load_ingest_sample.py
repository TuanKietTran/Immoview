from __future__ import annotations

import time

from django.core.management.base import BaseCommand

from apps.ingest.pipeline import ingest_payload


class Command(BaseCommand):
    help = "Load deterministic synthetic listings through the ingest pipeline."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=1000)
        parser.add_argument("--source", default="synthetic-benchmark")

    def handle(self, *args, **options):
        count = options["count"]
        if count < 1 or count > 100_000:
            raise ValueError("count must be between 1 and 100000")
        payloads = [
            {
                "external_id": f"sample-{index}",
                "title": f"Sample listing {index}",
                "description": "Synthetic benchmark listing",
                "price_vnd": 1_000_000_000 + index,
                "area_m2": 50,
                "province_code": "48",
                "commune_code": "48001",
            }
            for index in range(count)
        ]
        started = time.perf_counter()
        run = ingest_payload(options["source"], payloads)
        elapsed = time.perf_counter() - started
        self.stdout.write(
            self.style.SUCCESS(
                f"source={run.source} fetched={run.fetched_count} imported={run.imported_count} "
                f"errors={run.error_count} elapsed_s={elapsed:.3f} rows_per_s={count / elapsed:.1f}"
            )
        )
