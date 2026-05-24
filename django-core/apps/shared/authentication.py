import logging
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)


class JWTWithMembershipAuthentication(JWTAuthentication):
    """
    Extends simplejwt's JWTAuthentication to resolve active_membership_id
    from the token claims and attach the Membership to request.active_membership.
    Keeps permission classes simple — they just read request.active_membership.
    """

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None

        user, token = result
        request.active_membership = None

        membership_id = token.get("active_membership_id")
        if not membership_id:
            return user, token

        try:
            from apps.shared.models import Membership
            request.active_membership = (
                Membership.objects
                .select_related("agency", "user")
                .get(id=membership_id, is_active=True)
            )
        except Exception:
            logger.debug("active_membership_id %s not found or inactive", membership_id)

        return user, token
