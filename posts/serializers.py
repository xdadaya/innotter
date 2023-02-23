from rest_framework.serializers import ModelSerializer
from posts.models import Post
from users.serializers import UserSerializer


class PostSerializer(ModelSerializer):
    likes = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
