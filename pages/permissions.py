from rest_framework import permissions
from django.http import HttpRequest
from pages.models import Page


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: Page) -> bool:
        print('is owner')
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ("PUT", "PATCH", "DELETE"):
            return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: Page) -> bool:
        print('is mod')
        if request.method in ("PUT", "PATCH"):
            return request.user.role == "moderator"


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: Page) -> bool:
        print('is adm')
        return request.user.role == 'admin'
