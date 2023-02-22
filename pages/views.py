from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from pages.PageService import PageService
from pages.models import Page
from pages.serializers import PageSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import uuid
from pages.permissions import IsOwner, IsModerator, IsAdmin
from rest_framework.decorators import action
from django.http import HttpRequest


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner | IsModerator | IsAdmin)

    def perform_create(self, serializer: PageSerializer) -> None:
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["PATCH"], url_path='set-private')
    def set_private(self, request: HttpRequest, pk: uuid) -> Response:
        PageService.set_private(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path='set-public')
    def set_public(self, request: HttpRequest, pk: uuid) -> Response:
        PageService.set_public(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def follow(self, request: HttpRequest, pk: uuid) -> Response:
        PageService.follow(request.user, pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path="accept-all")
    def accept_all_requests(self, request: HttpRequest, pk: uuid) -> Response:
        PageService.accept_all_requests(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'accept-single/(?P<user_id>\d+)')
    def accept_single_request(self, request: HttpRequest, pk: uuid, user_id: uuid) -> Response:
        PageService.accept_single_request(pk, user_id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path='follow-requests')
    def follow_requests(self, request: HttpRequest, pk: uuid) -> Response:
        users = PageService.follow_requests(pk)
        return Response({"users": users}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'block/(?P<delta_days>\d+)')
    def block_page(self, request: HttpRequest, pk: uuid, delta_days: int) -> Response:
        PageService.block_page(pk, delta_days)
        return Response(status=status.HTTP_200_OK)
