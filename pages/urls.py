from rest_framework import routers
from pages.views import PageViewSet, FollowRequestViewSet


router = routers.SimpleRouter()
router.register(r'api/pages', PageViewSet, basename='page')
router.register(r'api/follows', FollowRequestViewSet, basename='follow_request')

urlpatterns = router.urls
