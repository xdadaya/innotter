from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from users.models import User


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: Post) -> bool:
        return request.user.role == User.Roles.ADMIN
