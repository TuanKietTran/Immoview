from rest_framework import viewsets, permissions
from apps.agencies.infrastructure.models import AgencyModel
from .serializers import AgencySerializer


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = AgencyModel.objects.filter(is_active=True)
    serializer_class = AgencySerializer
    search_fields = ["name", "email"]
    ordering_fields = ["name", "created_at", "subscription_tier"]
    ordering = ["name"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
