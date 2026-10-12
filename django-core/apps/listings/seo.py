from __future__ import annotations

from django.utils.text import slugify

from .infrastructure.models import ListingModel


def ensure_slug(listing: ListingModel) -> str:
    base = slugify(listing.title) or "listing"
    candidate = base
    suffix = str(listing.id)[:8]
    if not listing.slug:
        candidate = f"{base}-{suffix}"
        ListingModel.objects.filter(pk=listing.pk).update(slug=candidate)
        listing.slug = candidate
    return listing.slug
