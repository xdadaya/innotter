from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from pages.page_service import PageService
from pages.models import Page
from pages.serializers import PageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
import uuid
from pages.permissions import IsOwner, IsModerator, IsAdmin
from rest_framework.decorators import action
from django.http import HttpRequest
from shared.s3_service import S3Service


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def perform_create(self, serializer: PageSerializer) -> None:
        serializer.save(owner=self.request.user)

    def destroy(self, request: HttpRequest, *args, **kwargs) -> Response:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance: Page) -> None:
        if instance.image:
            file_key = instance.image[instance.image.rindex('/') + 1:]
            S3Service.delete_file(file_key)
        instance.delete()

    def get_permissions(self) -> BasePermission:
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
            'block_page_permanent': [IsAdmin],
            'search': [AllowAny]
        }
        return [permission() for permission in permissions.get(self.action, AllowAny)]

    @action(detail=True, methods=["PATCH"], url_path='set-private')
    def set_private(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.set_private(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path='set-public')
    def set_public(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.set_public(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def follow(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.follow(request.user, pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def unfollow(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.unfollow(request.user, pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="accept-all")
    def accept_all_requests(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.accept_all_requests(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="reject-all")
    def reject_all_requests(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.reject_all_requests(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path=r'accept-single/(?P<request_id>[^/.]+)')
    def accept_single_request(self, request: HttpRequest, pk: uuid.UUID, request_id: uuid.UUID) -> Response:
        PageService.accept_single_request(pk, request_id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path=r'reject-single/(?P<request_id>[^/.]+)')
    def reject_single_request(self, request: HttpRequest, pk: uuid.UUID, request_id: uuid.UUID) -> Response:
        PageService.reject_single_request(request_id)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], url_path='follow-requests')
    def follow_requests(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        users = PageService.follow_requests(pk)
        return Response({"users": users}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'block')
    def block_page(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        delta_days = request.data["delta_days"]
        PageService.block_page(pk, delta_days)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], url_path=r'permanent-block')
    def block_page_permanent(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PageService.block_page_permanent(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path='search')
    def search(self, request: HttpRequest) -> Response:
        pages = PageService.search(request.GET)
        return Response({"pages": pages}, status=status.HTTP_200_OK)
