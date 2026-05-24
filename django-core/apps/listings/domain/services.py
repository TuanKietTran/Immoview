from .entities import Listing, ListingStatus


def publish_listing(listing: Listing) -> None:
    listing.publish()


def archive_listing(listing: Listing) -> None:
    listing.archive()


def is_active(listing: Listing) -> bool:
    return listing.status in (ListingStatus.PUBLISHED, ListingStatus.RESERVED)
