from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.shared.views import jwks
from apps.shared.health import liveness, readiness, services as services_health

urlpatterns = [
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/listings/", include("apps.listings.api.urls")),
    path("api/v1/agencies/", include("apps.agencies.api.urls")),
    path("api/v1/leads/", include("apps.leads.api.urls")),
    path("api/v1/valuations/", include("apps.valuations.api.urls")),
    path("api/v1/billing/", include("apps.billing.api.urls")),
    # Auth — JWT tokens + web session
    path("api/v1/auth/token/", include("apps.shared.jwt_urls")),
    path("accounts/", include("allauth.urls")),
    # Health / control plane
    path("health/", liveness, name="health-liveness"),
    path("health/ready/", readiness, name="health-readiness"),
    path("health/services/", services_health, name="health-services"),
    # JWKS — RS256 public key for Lambda/external JWT verification
    path(".well-known/jwks.json", jwks, name="jwks"),
    # OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # MIS templates (internal)
    path("mis/", include("apps.agencies.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
