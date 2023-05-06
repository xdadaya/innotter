from django.urls import path
from rest_framework import routers

from users.views import RegistrationAPIView, LoginAPIView, ManageUserViewSet

router = routers.SimpleRouter()
router.register(r'api/users', ManageUserViewSet, basename='manage-users')

app_name = 'users'

urlpatterns = [
    path('api/register', RegistrationAPIView.as_view(), name='register'),
    path('api/login', LoginAPIView.as_view(), name='login')
]

urlpatterns += router.urls
