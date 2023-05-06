import json
import uuid
from typing import Any

from django.http import HttpRequest
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from innotter.producer import publish
from pages.models import Page
from pages.page_service import PageService
from pages.permissions import IsOwner, IsModerator, IsAdmin
from pages.serializers import PageSerializer
from shared.s3_service import S3Service


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'id', 'tags__name')

    def perform_create(self, serializer: PageSerializer) -> None:
        serializer.save(owner=self.request.user)

    def destroy(self, request: HttpRequest, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        instance = self.get_object()
        data = {
            "page_id": str(instance.id),
            "owner_id": str(instance.owner.id)
        }
        publish("delete_page", json.dumps(data))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance: Page) -> None:
        if instance.image:
            file_key = instance.image[instance.image.rindex('/') + 1:]
            S3Service.delete_file(file_key)
        instance.delete()

    def get_permissions(self) -> list[BasePermission]:
        permissions = {
            'list': [AllowAny],
            'create': [IsAuthenticated],
            'retrieve': [AllowAny],
            'update': [IsOwner | IsModerator | IsAdmin],
            'partial-update': [IsOwner | IsModerator | IsAdmin],
            'destroy': [IsOwner | IsModerator | IsAdmin],
            'follow': [IsAuthenticated],
            'unfollow': [IsAuthenticated],
            'set_private': [IsOwner],
            'set_public': [IsOwner],
            'accept_single_request': [IsOwner],
            'reject_single_request': [IsOwner],
            'accept_all_requests': [IsOwner],
            'reject_all_requests': [IsOwner],
            'follow_requests': [IsOwner],
            'block_page': [IsAdmin | IsModerator],
            'block_page_permanent': [IsAdmin]
        }
        return [permission() for permission in permissions.get(self.action, [IsAdmin])]

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated, IsOwner], url_path='set-private')
    def set_private(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.set_private(self.get_object().id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], permission_classes=[IsOwner], url_path='set-public')
    def set_public(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.set_public(self.get_object().id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def follow(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.follow(request.user, self.get_object().id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def unfollow(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.unfollow(request.user, self.get_object().id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="accept-all")
    def accept_all_requests(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.accept_all_requests(self.get_object().id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="reject-all")
    def reject_all_requests(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.reject_all_requests(self.get_object().id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path=r'accept-single/(?P<request_id>[^/.]+)')
    def accept_single_request(self, request: HttpRequest, pk: uuid.UUID, request_id: uuid.UUID) -> Response:
        PageService.accept_single_request(self.get_object().id, request_id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path=r'reject-single/(?P<request_id>[^/.]+)')
    def reject_single_request(self, request: HttpRequest, pk: uuid.UUID, request_id: uuid.UUID) -> Response:
        PageService.reject_single_request(request_id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path='follow-requests')
    def follow_requests(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        users = PageService.follow_requests(self.get_object().id)
        return Response({"users": users}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'block')
    def block_page(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        delta_days = request.data["delta_days"]
        PageService.block_page(self.get_object().id, delta_days)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'permanent-block')
    def block_page_permanent(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.block_page_permanent(self.get_object().id)
        return Response(status=status.HTTP_200_OK)
