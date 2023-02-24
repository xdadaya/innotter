from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from shared.s3service import S3Service


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    image_s3_path = serializers.URLField(read_only=True)
    uploaded_image = serializers.ImageField(max_length=64, write_only=True, required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'uploaded_image', 'image_s3_path')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data: dict[str, str]) -> User:
        img = validated_data.pop("uploaded_image") if "uploaded_image" in validated_data.keys() else None
        user = User.objects.create_user(**validated_data)
        if img:
            user.image_s3_path = S3Service.upload_file(img)
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data) -> dict[str, str]:
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex')

    class Meta:
        model = User
        fields = ("id", "username", "role")
