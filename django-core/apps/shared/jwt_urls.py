from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .jwt_backend import ImmoviewTokenObtainPairView

urlpatterns = [
    path("", ImmoviewTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]
