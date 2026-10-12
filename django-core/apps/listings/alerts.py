from __future__ import annotations

from apps.listings.infrastructure.models import ListingModel, SavedSearchModel
from apps.shared.notifications import dispatch_notification


def listing_matches_saved_search(listing: ListingModel, saved_search: SavedSearchModel) -> bool:
    query = saved_search.query or {}
    if query.get("province_code") and query["province_code"] != listing.province_code:
        return False
    if query.get("commune_code") and query["commune_code"] != listing.commune_code:
        return False
    if query.get("offer_type") and query["offer_type"] != listing.offer_type:
        return False
    if query.get("property_type") and query["property_type"] != listing.property_type:
        return False
    if query.get("max_price_vnd") is not None and listing.price_vnd is not None and listing.price_vnd > int(query["max_price_vnd"]):
        return False
    return not (query.get("min_area_m2") is not None and listing.area_m2 < float(query["min_area_m2"]))


def dispatch_listing_alerts(listing: ListingModel) -> int:
    sent = 0
    searches = SavedSearchModel.objects.filter(active=True)
    for saved_search in searches.iterator():
        if listing_matches_saved_search(listing, saved_search):
            dispatch_notification(
                "saved_search.match",
                {
                    "user_id": str(saved_search.user_id),
                    "saved_search_id": str(saved_search.id),
                    "listing_id": str(listing.id),
                    "listing_title": listing.title,
                },
            )
            sent += 1
    return sent
