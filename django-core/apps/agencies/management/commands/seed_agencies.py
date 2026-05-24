import random
from django.core.management.base import BaseCommand
from faker import Faker

from apps.agencies.infrastructure.models import AgencyModel
from apps.agencies.domain.entities import SubscriptionTier

fake = Faker("de_CH")

CANTONS = ["ZH", "BE", "BS", "GE", "VD", "LU", "SG", "GR", "TI", "AG"]


class Command(BaseCommand):
    help = "Seed fake agency data"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10)

    def handle(self, *args, **options):
        count = options["count"]
        created = 0
        for _ in range(count):
            canton = random.choice(CANTONS)
            tier = random.choices(
                list(SubscriptionTier),
                weights=[20, 40, 30, 10],
            )[0]
            AgencyModel.objects.create(
                name=f"{fake.last_name()} Immobilien {fake.city()[:8]}",
                email=fake.unique.email(),
                phone=fake.phone_number(),
                canton=canton,
                subscription_tier=tier.value,
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} agencies"))
