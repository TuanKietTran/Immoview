from __future__ import annotations

from uuid import UUID

from django.db import transaction

from apps.listings.domain.entities import ListingStatus
from apps.listings.infrastructure.models import ListingAuditEvent, ListingModel


ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    ListingStatus.DRAFT.value: frozenset({ListingStatus.PENDING_REVIEW.value, ListingStatus.ARCHIVED.value}),
    ListingStatus.PENDING_REVIEW.value: frozenset({ListingStatus.PUBLISHED.value, ListingStatus.DRAFT.value}),
    ListingStatus.PUBLISHED.value: frozenset({ListingStatus.RESERVED.value, ListingStatus.SOLD.value, ListingStatus.RENTED.value, ListingStatus.EXPIRED.value, ListingStatus.ARCHIVED.value}),
    ListingStatus.RESERVED.value: frozenset({ListingStatus.SOLD.value, ListingStatus.RENTED.value, ListingStatus.PUBLISHED.value, ListingStatus.EXPIRED.value}),
    ListingStatus.SOLD.value: frozenset({ListingStatus.ARCHIVED.value}),
    ListingStatus.RENTED.value: frozenset({ListingStatus.ARCHIVED.value}),
    ListingStatus.EXPIRED.value: frozenset({ListingStatus.ARCHIVED.value}),
    ListingStatus.ARCHIVED.value: frozenset({ListingStatus.DRAFT.value}),
}


class InvalidListingTransition(ValueError):
    pass


@transaction.atomic
def transition_listing(
    listing_id: UUID,
    to_status: str,
    *,
    actor_id: UUID | None = None,
    reason: str = "",
    metadata: dict | None = None,
) -> ListingModel:
    """Atomically enforce the lifecycle and append an immutable audit event."""
    listing = ListingModel.objects.select_for_update().get(pk=listing_id)
    allowed = ALLOWED_TRANSITIONS.get(listing.status, frozenset())
    if to_status not in allowed:
        raise InvalidListingTransition(f"Cannot transition {listing.status} -> {to_status}")
    previous = listing.status
    listing.status = to_status
    listing.save(update_fields=["status", "updated_at"])
    ListingAuditEvent.objects.create(
        listing=listing,
        from_status=previous,
        to_status=to_status,
        actor_id=actor_id,
        reason=reason,
        metadata=metadata or {},
    )
    return listing
