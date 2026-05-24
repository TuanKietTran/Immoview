import logging
from rest_framework.views import exception_handler as _drf_handler

logger = logging.getLogger(__name__)


def sentry_exception_handler(exc, context):
    """
    DRF exception handler that enriches Sentry with IAM context on 403.
    Scrubs all PII (email, name) — only role and agency_id are tagged.
    """
    response = _drf_handler(exc, context)

    if response is not None and response.status_code == 403:
        try:
            import sentry_sdk
            request = context.get("request")
            if request is None:
                return response

            membership = getattr(request, "active_membership", None)
            user = getattr(request, "user", None)

            with sentry_sdk.new_scope() as scope:
                scope.set_tag("http.status_code", 403)
                scope.set_tag("exception.type", type(exc).__name__)
                if membership:
                    scope.set_tag("agency.id", str(membership.agency_id))
                    scope.set_tag("user.role", membership.role)
                if user and user.is_authenticated:
                    scope.set_user({"id": str(user.id)})
                sentry_sdk.capture_exception(exc)
        except Exception:
            pass

    return response
