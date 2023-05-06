from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from users.models import User


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: Post) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in "DELETE":
            return obj.page.owner == request.user or request.user.role in (User.Roles.MODERATOR, User.Roles.ADMIN)
        return obj.page.owner == request.user
