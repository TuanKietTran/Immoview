from __future__ import annotations

from datetime import timedelta
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from .infrastructure.models import LeadActivity, LeadModel


@transaction.atomic
def route_lead(lead_id: UUID, agent_ids: list[UUID], sla_minutes: int = 30) -> LeadModel:
    """Assign the least-loaded candidate, breaking ties deterministically."""
    if not agent_ids:
        raise ValueError("At least one agent is required")
    lead = LeadModel.objects.select_for_update().get(pk=lead_id)
    loads = {
        agent_id: LeadModel.objects.filter(
            agency_id=lead.agency_id, assigned_agent_id=agent_id, status__in=["new", "contacted", "qualified"]
        ).count()
        for agent_id in agent_ids
    }
    selected = min(agent_ids, key=lambda agent_id: (loads[agent_id], str(agent_id)))
    lead.assigned_agent_id = selected
    lead.sla_due_at = timezone.now() + timedelta(minutes=sla_minutes)
    lead.save(update_fields=["assigned_agent_id", "sla_due_at", "updated_at"])
    LeadActivity.objects.create(lead=lead, activity_type="assigned", note=f"agent={selected}")
    return lead
