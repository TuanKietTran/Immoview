from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.shared.metrics import increment


class ImmoviewTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        membership = (
            user.memberships
            .filter(is_active=True)
            .select_related("agency")
            .order_by("-joined_at")
            .first()
        )
        if membership:
            token["active_membership_id"] = str(membership.id)
            token["role"] = membership.role
            token["agency_id"] = str(membership.agency_id)

        token["is_staff_immoview"] = user.is_staff_immoview
        role = membership.role if membership else "none"
        increment("immoview.jwt.issued", tags=[f"role:{role}"])
        return token


class ImmoviewTokenObtainPairView(TokenObtainPairView):
    serializer_class = ImmoviewTokenObtainPairSerializer
