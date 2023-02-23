from rest_framework import routers
from pages.views import PageViewSet


router = routers.SimpleRouter()
router.register(r'api/pages', PageViewSet, basename='page')

urlpatterns = router.urls
