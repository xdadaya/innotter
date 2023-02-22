from rest_framework import serializers
from pages.models import Page
from users.serializers import UserSerializer
from tags.serializers import TagSerializer
from tags.models import Tag


class PageSerializer(serializers.ModelSerializer):
    image = serializers.URLField(read_only=True)
    uploaded_image = serializers.ImageField(max_length=64, write_only=True, required=False)
    uuid = serializers.CharField(read_only=True)
    owner = UserSerializer(read_only=True)
    uploaded_tags = serializers.ListField(child=serializers.CharField(max_length=30), write_only=True)
    tags = TagSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)
    follow_requests = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = "__all__"

    def create(self, validated_data: dict[str, str]) -> Page:
        tags_names = validated_data.pop("uploaded_tags")
        page = Page.objects.create(**validated_data)
        for tag_name in tags_names:
            tag = Tag.objects.get_or_create(name=tag_name)[0]
            page.tags.add(TagSerializer(tag).data["id"])
        return page

    def update(self, instance: Page, validated_data: dict[str, str]) -> Page:
        tags_names = validated_data.pop("uploaded_tags")
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('name', instance.description)
        instance.tags.clear()
        for tag_name in tags_names:
            tag = Tag.objects.get_or_create(name=tag_name)[0]
            instance.tags.add(TagSerializer(tag).data["id"])
        instance.save()
        return instance
