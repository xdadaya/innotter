from django.contrib.auth import authenticate
from rest_framework import serializers

from shared.s3_service import S3Service
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    image_s3_path = serializers.URLField(read_only=True)
    uploaded_image = serializers.ImageField(max_length=64, write_only=True, required=False)
    title = serializers.CharField(max_length=80, required=False)
    role = serializers.ChoiceField([User.Roles.USER, User.Roles.MODERATOR, User.Roles.ADMIN], required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'uploaded_image', 'image_s3_path', 'title', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data: dict[str, str]) -> User:
        img = validated_data.pop("uploaded_image", None)
        title = validated_data.pop("title", None)
        role = validated_data.pop("role", 'user')
        user = User.objects.create_user(**validated_data)
        user.title = title
        user.role = role
        if role == User.Roles.ADMIN:
            user.is_staff = True
            user.is_superuser = True
        if img:
            user.image_s3_path = S3Service.upload_file(img)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data) -> dict[str, str]:
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None:
            raise serializers.ValidationError(
                'Username is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        if user.is_blocked:
            raise serializers.ValidationError(
                'A user with this username is blocked'
            )

        return {
            'username': user.username,
            'id': user.id
        }


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    title = serializers.CharField()

    class Meta:
        model = User
        fields = ("id", "username", "role", "title")
