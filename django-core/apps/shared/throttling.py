from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class PublicRateThrottle(AnonRateThrottle):
    scope = "public"


class AuthenticatedRateThrottle(UserRateThrottle):
    scope = "authenticated"
