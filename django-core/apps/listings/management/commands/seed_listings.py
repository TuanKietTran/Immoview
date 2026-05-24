import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker

from apps.listings.infrastructure.models import ListingModel
from apps.listings.domain.entities import PropertyType, OfferType, ListingStatus

fake = Faker("de_CH")

SWISS_CITIES = [
    ("8001", "Zürich", "ZH"),
    ("3001", "Bern", "BE"),
    ("4001", "Basel", "BS"),
    ("1200", "Genève", "GE"),
    ("1000", "Lausanne", "VD"),
    ("6003", "Luzern", "LU"),
    ("9000", "St. Gallen", "SG"),
    ("7000", "Chur", "GR"),
    ("6900", "Lugano", "TI"),
    ("5000", "Aarau", "AG"),
]


class Command(BaseCommand):
    help = "Seed fake listing data with Swiss postcodes and CHF prices"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=50)
        parser.add_argument("--agency-id", type=str, default=None)

    def handle(self, *args, **options):
        import uuid
        count = options["count"]
        agency_id = options["agency_id"] or str(uuid.uuid4())

        created = 0
        for _ in range(count):
            postcode, city, canton = random.choice(SWISS_CITIES)
            offer = random.choice(list(OfferType))
            prop = random.choice(list(PropertyType))

            if offer == OfferType.RENT:
                price = Decimal(random.randrange(1200, 8000, 100))
            else:
                price = Decimal(random.randrange(350_000, 4_500_000, 50_000))

            rooms = random.choice([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0])
            area = round(rooms * random.uniform(28, 42), 1)

            ListingModel.objects.create(
                agency_id=agency_id,
                title=f"{rooms:.0f}.5-Zimmer {prop.value.title()} in {city}",
                description=fake.paragraph(nb_sentences=4),
                property_type=prop.value,
                offer_type=offer.value,
                street=fake.street_name(),
                street_number=str(random.randint(1, 120)),
                postcode=postcode,
                city=city,
                canton=canton,
                price_chf=price,
                area_m2=area,
                rooms=rooms,
                status=random.choice([
                    ListingStatus.PUBLISHED.value,
                    ListingStatus.PUBLISHED.value,
                    ListingStatus.PUBLISHED.value,
                    ListingStatus.RESERVED.value,
                    ListingStatus.DRAFT.value,
                ]),
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} listings (agency={agency_id})"))
