import time
import uuid

from django.core.management.base import BaseCommand

from apps.listings.infrastructure.models import ListingModel


class Command(BaseCommand):
    help = "Import deterministic synthetic listings idempotently for throughput verification."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=100_000)
        parser.add_argument("--batch-size", type=int, default=2_000)

    def handle(self, *args, **options):
        count = options["count"]
        batch_size = options["batch_size"]
        started = time.perf_counter()
        rows = [
            ListingModel(
                source_external_id=f"synthetic:{index}", agency_id=uuid.UUID(int=0), title=f"Synthetic {index}",
                description="Synthetic throughput fixture", property_type="house", offer_type="sale",
                street="Fixture", street_number=str(index), postcode="5500", city="Da Nang", canton="VN",
                price_chf=0, price_vnd=1_000_000_000, area_m2=80,
            )
            for index in range(count)
        ]
        for start in range(0, count, batch_size):
            ListingModel.objects.bulk_create(rows[start:start + batch_size], batch_size=batch_size, ignore_conflicts=True)
        elapsed = time.perf_counter() - started
        total = ListingModel.objects.filter(source_external_id__startswith="synthetic:").count()
        self.stdout.write(f"requested={count} total={total} elapsed_seconds={elapsed:.3f}")
