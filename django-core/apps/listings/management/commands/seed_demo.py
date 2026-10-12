from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create development-only demo listings (never use in production)."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=20)
        parser.add_argument("--agency-id", type=str, default=None)

    def handle(self, *args, **options):
        call_command(
            "seed_listings",
            count=options["count"],
            agency_id=options["agency_id"],
        )
