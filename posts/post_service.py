import json
import uuid

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from innotter.producer import publish
from pages.models import Page
from posts.models import Post, Like
from posts.serializers import PostSerializer
from users.models import User


class PostService:
    @staticmethod
    def like(pk: uuid.UUID, user: User) -> None:
        post = Post.objects.get(id=pk)
        is_created = Like.objects.get_or_create(user=user, post=post)[1]
        if is_created:
            post.likes_amount += 1
            post.save()
            likes_amount = Post.objects.filter(page=post.page.id).aggregate(sum=Sum('likes_amount'))['sum']
            data = {
                "page_id": str(post.page.id),
                "owner_id": str(post.page.owner.id),
                "likes_amount": likes_amount
            }
            publish("update_page", json.dumps(data))

    @staticmethod
    def dislike(pk: uuid.UUID, user: User) -> None:
        post = Post.objects.get(id=pk)
        like = get_object_or_404(Like, user=user, post=post)
        post.likes_amount -= 1
        like.delete()
        post.save()
        likes_amount = Post.objects.filter(page=post.page.id).aggregate(sum=Sum('likes_amount'))['sum']
        data = {
            "page_id": str(post.page.id),
            "owner_id": str(post.page.owner.id),
            "likes_amount": likes_amount
        }
        publish("update_page", json.dumps(data))

    @staticmethod
    def feed(user: User) -> list[Post]:
        pages_pks_owners = Page.objects.filter(owner=user)
        pages_pks_followers = Page.objects.filter(followers=user)
        pages_pks = pages_pks_owners | pages_pks_followers
        posts = PostSerializer(Post.objects.filter(page__in=pages_pks), many=True)
        return posts.data

    @staticmethod
    def liked(user: User) -> list[Post]:
        posts_pks = Like.objects.filter(user=user).values_list('post_id', flat=True)
        posts = PostSerializer(Post.objects.filter(id__in=posts_pks), many=True)
        return posts.data
