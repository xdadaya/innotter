from users.models import User
from posts.models import Post
import uuid


class PostService:
    @staticmethod
    def like(pk: uuid.UUID, user: User) -> None:
        print(user)
        post = Post.objects.get(id=pk)
        post.likes.add(user)

    @staticmethod
    def dislike(pk: uuid.UUID, user: User) -> None:
        post = Post.objects.get(id=pk)
        post.likes.remove(user)
