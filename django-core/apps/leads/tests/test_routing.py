import uuid

import pytest
from django.utils import timezone

from apps.leads.application import route_lead
from apps.leads.infrastructure.models import LeadActivity, LeadModel, ViewingSlot


@pytest.fixture
def lead(db: None) -> LeadModel:
    return LeadModel.objects.create(
        listing_id=uuid.uuid4(), agency_id=uuid.uuid4(), name="A", email="a@example.com",
        phone="0901", message="Interested", source="website",
    )


@pytest.mark.django_db
def test_round_robin_route_picks_least_loaded_agent(lead: LeadModel) -> None:
    first, second = uuid.uuid4(), uuid.uuid4()
    routed = route_lead(lead.id, [first, second], sla_minutes=15)
    assert routed.assigned_agent_id == min(first, second, key=str)
    assert routed.sla_due_at > timezone.now()
    assert LeadActivity.objects.filter(lead=lead, activity_type="assigned").count() == 1


@pytest.mark.django_db
def test_viewing_slot_requires_positive_duration(lead: LeadModel) -> None:
    now = timezone.now()
    slot = ViewingSlot(lead=lead, agent_id=uuid.uuid4(), starts_at=now, ends_at=now)
    with pytest.raises(Exception):
        slot.full_clean()
