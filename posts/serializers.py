import json

from rest_framework.serializers import ModelSerializer

from innotter.producer import publish
from posts.models import Post
from users.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    likes = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        posts_amount = Post.objects.filter(page=post.page).count()
        data = {
            "page_id": str(post.page.id),
            "owner_id": str(post.page.owner.id),
            "posts_amount": posts_amount,
        }
        publish("update_page", json.dumps(data))
        return post
