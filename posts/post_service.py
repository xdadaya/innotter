from users.models import User
from posts.models import Post, Like
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
