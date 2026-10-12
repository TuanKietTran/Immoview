from __future__ import annotations

from uuid import UUID

from django.db import transaction
from django.utils import timezone

from .infrastructure.models import AgencyModel, AgencyStatus


class InvalidAgencyTransition(ValueError):
    pass


@transaction.atomic
def submit_for_approval(agency_id: UUID) -> AgencyModel:
    agency = AgencyModel.objects.select_for_update().get(pk=agency_id)
    if agency.status != AgencyStatus.ONBOARDING:
        raise InvalidAgencyTransition("Only onboarding agencies can be submitted")
    agency.status = AgencyStatus.PENDING_APPROVAL
    agency.save(update_fields=["status", "updated_at"])
    return agency


@transaction.atomic
def approve_agency(agency_id: UUID, approver_id: UUID) -> AgencyModel:
    agency = AgencyModel.objects.select_for_update().get(pk=agency_id)
    if agency.status != AgencyStatus.PENDING_APPROVAL:
        raise InvalidAgencyTransition("Only pending agencies can be approved")
    agency.status = AgencyStatus.APPROVED
    agency.is_active = True
    agency.approved_at = timezone.now()
    agency.approved_by_id = approver_id
    agency.save(update_fields=["status", "is_active", "approved_at", "approved_by_id", "updated_at"])
    return agency
