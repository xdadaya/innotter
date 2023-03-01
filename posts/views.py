from rest_framework.viewsets import ModelViewSet
from posts.models import Post
from pages.models import Page
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from posts.permissions import IsOwnerOrStaff
from rest_framework.decorators import action
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from posts.post_service import PostService
from tasks.send_email import send_emails
import uuid


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrStaff)

    def perform_create(self, serializer: PostSerializer) -> None:
        emails = Page.objects.get(id=serializer.data["page"]).followers.values_list("email", flat=True)
        base_domain = self.request.get_host()
        send_emails.send(emails=list(emails), base_domain=base_domain)

    @action(detail=True, methods=["POST"], url_path=r'like')
    def like(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PostService.like(pk, request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path=r'dislike')
    def dislike(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PostService.dislike(pk, request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path=r'liked', permission_classes=(IsAuthenticated, ))
    def liked(self, request: HttpRequest) -> Response:
        posts = PostService.liked(request.user)
        return Response({"posts": posts}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path=r'feed', permission_classes=(IsAuthenticated,))
    def feed(self, request: HttpRequest) -> Response:
        posts = PostService.feed(request.user)
        return Response({"posts": posts}, status=status.HTTP_200_OK)


