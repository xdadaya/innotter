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
        serializer.save(uuid=str(uuid.uuid4()), owner=self.request.user)

    @action(detail=True, methods=["PATCH"], url_path='set-private')
    def setPrivate(self, request: HttpRequest, pk: int) -> Response:
        PageService.setPrivate(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path='set-public')
    def setPublic(self, request: HttpRequest, pk: int) -> Response:
        Page.objects.filter(id=pk).update(is_private=False)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def follow(self, request: HttpRequest, pk: int) -> Response:
        PageService.follow(request, pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path="accept-all")
    def acceptAllRequests(self, request: HttpRequest, pk: int) -> Response:
        PageService.acceptAllRequests(request, pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'accept-single/(?P<user_id>\d+)')
    def acceptSingleRequest(self, request: HttpRequest, pk: int, user_id: int) -> Response:
        PageService.acceptSingleRequest(request, pk, user_id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path='follow-requests')
    def followRequests(self, request: HttpRequest, pk: int) -> Response:
        users = PageService.followRequests(pk)
        return Response({"users": users}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'block/(?P<delta_days>\d+)')
    def blockPage(self, request: HttpRequest, pk: int, delta_days: int) -> Response:
        PageService.blockPage(pk, delta_days)
        return Response(status=status.HTTP_200_OK)