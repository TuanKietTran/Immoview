from django.urls import path
from . import views

urlpatterns = [
    path("", views.mis_dashboard, name="mis-dashboard"),
    path("agencies/<uuid:agency_id>/", views.agency_detail, name="agency-detail"),
]
