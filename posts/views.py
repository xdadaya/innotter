from rest_framework.viewsets import ModelViewSet
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from posts.permissions import IsOwnerOrStaff
from rest_framework.decorators import action
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from posts.post_service import PostService
import uuid


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrStaff)

    @action(detail=True, methods=["POST"], url_path=r'like')
    def like(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PostService.like(pk, request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path=r'dislike')
    def dislike(self, request: HttpRequest, pk: uuid.UUID) -> Response:
        PostService.dislike(pk, request.user)
        return Response(status=status.HTTP_200_OK)


