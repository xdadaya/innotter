from rest_framework import serializers

from pages.models import Page, FollowRequest
from shared.s3_service import S3Service
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class FollowRequestSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = FollowRequest
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    image = serializers.URLField(read_only=True)
    uploaded_image = serializers.ImageField(max_length=64, write_only=True, required=False)
    uuid = serializers.CharField(read_only=True)
    owner = UserSerializer(read_only=True)
    uploaded_tags = serializers.ListField(child=serializers.CharField(max_length=30), write_only=True)
    tags = TagSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)
    follow_requests = FollowRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = "__all__"

    def create(self, validated_data: dict[str, str]) -> Page:
        img = validated_data.pop("uploaded_image", None)
        tags_names = validated_data.pop("uploaded_tags")
        page = Page.objects.create(**validated_data)
        if img:
            page.image = S3Service.upload_file(img)
        for tag_name in tags_names:
            tag = Tag.objects.get_or_create(name=tag_name)[0]
            page.tags.add(tag.id)
        return page

    def update(self, instance: Page, validated_data: dict[str, str]) -> Page:
        img = validated_data.pop("uploaded_image", None)
        tags_names = validated_data.pop("uploaded_tags")
        instance.name = validated_data.get('name', instance.name)
        if instance.image:
            file_key = instance.image[instance.image.rindex('/') + 1:]
            S3Service.delete_file(file_key)
        if img:
            instance.image = S3Service.upload_file(img)
        instance.description = validated_data.get('name', instance.description)
        instance.tags.clear()
        for tag_name in tags_names:
            tag = Tag.objects.get_or_create(name=tag_name)[0]
            instance.tags.add(tag.id)
        instance.save()
        return instance
