from django.urls import path
from .views import ValuationEstimateView

urlpatterns = [
    path("estimate/", ValuationEstimateView.as_view(), name="valuation-estimate"),
]
