import logging
from typing import Optional

logger = logging.getLogger(__name__)


def log_action(
    *,
    action: str,
    resource_type: str,
    resource_id: str,
    request=None,
    agency_id=None,
    membership=None,
) -> None:
    """
    Append an AuditLog entry. Fails silently — never break the calling flow.
    Call at the service layer, not in Django signals (signals miss bulk ops).
    """
    from .models import AuditLog

    try:
        actor_user_id = None
        actor_membership_id = None
        ip = None
        user_agent = ""
        trace_id = ""

        if request is not None:
            user = getattr(request, "user", None)
            if user and user.is_authenticated:
                actor_user_id = user.id
            active = getattr(request, "active_membership", None) or membership
            if active:
                actor_membership_id = active.id
                if agency_id is None:
                    agency_id = active.agency_id
            ip = _get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
            try:
                from ddtrace import tracer
                span = tracer.current_span()
                if span:
                    trace_id = str(span.trace_id)
            except Exception:
                pass

        AuditLog.objects.create(
            actor_user_id=actor_user_id,
            actor_membership_id=actor_membership_id,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id),
            agency_id=agency_id,
            ip=ip,
            user_agent=user_agent,
            trace_id=trace_id,
        )
    except Exception:
        logger.exception(
            "audit log write failed — action=%s resource=%s/%s",
            action, resource_type, resource_id,
        )


def _get_client_ip(request) -> Optional[str]:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")
