from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from pages.models import Page
from users.models import User


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: Page) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ("PUT", "PATCH", "DELETE"):
            return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: Page) -> bool:
        if request.method in ("PUT", "PATCH"):
            return request.user.role == User.Roles.MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: Page) -> bool:
        return request.user.role == User.Roles.ADMIN
