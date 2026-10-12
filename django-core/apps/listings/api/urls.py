from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, SavedSearchViewSet

router = DefaultRouter()
router.register(r"saved-searches", SavedSearchViewSet, basename="saved-search")
router.register(r"", ListingViewSet, basename="listing")

urlpatterns = router.urls
