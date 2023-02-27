from rest_framework import routers
from django.urls import path
from users.views import RegistrationAPIView, LoginAPIView, BlockUsersViewSet

router = routers.SimpleRouter()
router.register(r'api/users', BlockUsersViewSet, basename='manage-users')

app_name = 'users'

urlpatterns = [
    path('api/register', RegistrationAPIView.as_view(), name='register'),
    path('api/login', LoginAPIView.as_view(), name='login')
]

urlpatterns += router.urls
