import json
import uuid
from typing import Any

from django.db.models import Sum
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from innotter.producer import publish
from pages.models import Page
from posts.models import Post
from posts.permissions import IsOwnerOrStaff
from posts.post_service import PostService
from posts.serializers import PostSerializer
from shared.ses_service import SESService


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrStaff)

    def perform_create(self, serializer: PostSerializer) -> None:
        serializer.save()
        emails = Page.objects.get(id=serializer.data["page"]).followers.values_list("email", flat=True)
        base_domain = self.request.get_host()
        if emails:
            SESService.send_emails.delay(emails=list(emails), base_domain=base_domain,
                                         post_content=serializer.data["content"], page_id=serializer.data["page"])

    def destroy(self, request: HttpRequest, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        instance = self.get_object()
        page_id = instance.page
        self.perform_destroy(instance)
        posts_count = Post.objects.filter(page=page_id).count()
        likes_amount = Post.objects.filter(page=page_id).aggregate(sum=Sum('likes_amount'))['sum']
        if likes_amount is None:
            likes_amount = 0
        data = {
            "page_id": str(instance.page.id),
            "owner_id": str(instance.page.owner.id),
            "posts_amount": posts_count,
            "likes_amount": likes_amount
        }
        publish("update_page", json.dumps(data))
        return Response(status=status.HTTP_200_OK)

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


