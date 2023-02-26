from rest_framework import routers
from pages.views import PageViewSet, FollowRequestViewSet


router = routers.SimpleRouter()
router.register(r'api/pages', viewset=PageViewSet, basename='page')

urlpatterns = router.urls
