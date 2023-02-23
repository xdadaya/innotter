from rest_framework import permissions
from django.http import HttpRequest
from pages.models import Page, FollowRequest
from rest_framework.viewsets import ModelViewSet
from users.userABC import UserABC


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: Page) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ("PUT", "PATCH", "DELETE"):
            return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: Page) -> bool:
        if request.method in ("PUT", "PATCH"):
            return request.user.role == UserABC.Roles.MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: Page) -> bool:
        return request.user.role == UserABC.Roles.ADMIN


class FollowerRequestManage(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: ModelViewSet, obj: FollowRequest) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return obj.follower == request.user or obj.page.owner == request.user or request.user.role in (
                UserABC.Roles.MODERATOR, UserABC.Roles.ADMIN)
        return False
