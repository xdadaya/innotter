from rest_framework import routers

from posts.views import PostViewSet

router = routers.SimpleRouter()
router.register(r'api/posts', PostViewSet, basename='post')

urlpatterns = router.urls
