from users.models import User
from posts.models import Post, Like
from pages.models import Page
from posts.serializers import PostSerializer
from django.shortcuts import get_object_or_404
import uuid


class PostService:
    @staticmethod
    def like(pk: uuid.UUID, user: User) -> None:
        post = Post.objects.get(id=pk)
        is_created = Like.objects.get_or_create(user=user, post=post)[1]
        if is_created:
            post.likes_amount += 1
            post.save()

    @staticmethod
    def dislike(pk: uuid.UUID, user: User) -> None:
        post = Post.objects.get(id=pk)
        like = get_object_or_404(Like, user=user, post=post)
        post.likes_amount -= 1
        like.delete()
        post.save()

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
