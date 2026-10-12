from __future__ import annotations

from uuid import UUID

from apps.leads.infrastructure.models import LeadModel
from apps.listings.infrastructure.models import ListingModel
from apps.shared.models import Membership


def can_add_seat(agency_id: UUID) -> bool:
    agency = Membership.objects.select_related("agency").filter(agency_id=agency_id).first()
    if not agency:
        from apps.agencies.infrastructure.models import AgencyModel
        agency_obj = AgencyModel.objects.get(pk=agency_id)
    else:
        agency_obj = agency.agency
    return Membership.objects.filter(agency_id=agency_id, is_active=True).count() < agency_obj.seat_limit


def agent_stats(agent_id: UUID) -> dict[str, int]:
    membership = Membership.objects.filter(user_id=agent_id, is_active=True).first()
    agency_id = membership.agency_id if membership else None
    return {
        "active_leads": LeadModel.objects.filter(assigned_agent_id=agent_id, status__in=["new", "contacted", "qualified"]).count(),
        "won_leads": LeadModel.objects.filter(assigned_agent_id=agent_id, status="closed_won").count(),
        "published_listings": ListingModel.objects.filter(agency_id=agency_id, status="published").count() if agency_id else 0,
    }
