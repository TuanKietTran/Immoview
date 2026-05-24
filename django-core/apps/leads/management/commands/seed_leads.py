import random
from django.core.management.base import BaseCommand
from faker import Faker

from apps.leads.infrastructure.models import LeadModel
from apps.leads.domain.entities import LeadStatus, LeadSource
from apps.listings.infrastructure.models import ListingModel
from apps.agencies.infrastructure.models import AgencyModel

fake = Faker("de_CH")


class Command(BaseCommand):
    help = "Seed fake lead data"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=100)

    def handle(self, *args, **options):
        count = options["count"]
        listings = list(ListingModel.objects.values_list("id", "agency_id")[:200])
        if not listings:
            self.stdout.write(self.style.ERROR("No listings found — run seed_listings first"))
            return

        statuses = [s.value for s in LeadStatus]
        sources = [s.value for s in LeadSource]
        created = 0

        for _ in range(count):
            listing_id, agency_id = random.choice(listings)
            LeadModel.objects.create(
                listing_id=listing_id,
                agency_id=agency_id,
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                message=fake.sentence(nb_words=12),
                source=random.choice(sources),
                status=random.choice(statuses),
                score=random.randint(10, 95) if random.random() > 0.3 else None,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} leads"))
