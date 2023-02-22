from rest_framework import serializers
from pages.models import Page
from users.serializers import UserSerializer
from tags.serializers import TagSerializer
from tags.models import Tag


class PageSerializer(serializers.ModelSerializer):
    image = serializers.URLField(read_only=True)
    uploaded_image = serializers.ImageField(max_length=1000000, write_only=True, required=False)
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
        tags = validated_data.pop("uploaded_tags")
        all_created_tags = Tag.objects.all()
        all_created_tags_names = list(map(lambda x: x.name, Tag.objects.all()))
        page = Page.objects.create(**validated_data)
        for tag in tags:
            if tag not in all_created_tags_names:
                new_tag = Tag.objects.create(name=tag)
                page.tags.add(new_tag)
            else:
                page.tags.add(list(all_created_tags.filter(name=tag).values_list('pk', flat=True))[0])
        return page

    def update(self, instance: Page, validated_data: dict[str, str]) -> Page:
        tags = validated_data.pop("uploaded_tags")
        all_created_tags = Tag.objects.all()
        all_created_tags_names = list(map(lambda x: x.name, Tag.objects.all()))
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('name', instance.description)
        instance.tags.clear()
        for tag in tags:
            if tag not in all_created_tags_names:
                new_tag = Tag.objects.create(name=tag)
                instance.tags.add(new_tag)
            else:
                instance.tags.add(list(all_created_tags.filter(name=tag).values_list('pk', flat=True))[0])
        instance.save()
        return instance
