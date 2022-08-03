from rest_framework import serializers

from api.functions import get_today
from api.models import Post, User


class post_serializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    profile_name = serializers.CharField(source="created_by.get_name", read_only=True)
    profile_username = serializers.CharField(source="created_by.username", read_only=True)
    profile_image = serializers.ImageField(source="created_by.prof_image", read_only=True)
    content = serializers.CharField(default="")
    likes = serializers.IntegerField(default=0)
    comments = serializers.IntegerField(default=0)
    shares = serializers.IntegerField(default=0)
    status = serializers.IntegerField(default=0)
    image_post = serializers.BooleanField(default=False)
    image_contents = serializers.ImageField(default="")
    created_date = serializers.DateTimeField(required=False, allow_null=True, default=get_today)
    last_edit = serializers.DateTimeField(required=False, allow_null=True, default=get_today)
    last_update = serializers.DateTimeField(required=False, allow_null=True, default=get_today)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.created_date = validated_data.get('created_date', instance.created_date)
        instance.last_edit = validated_data.get('last_edit', instance.last_edit)
        instance.content = validated_data.get('content', instance.content)
        instance.likes = validated_data.get('likes', instance.likes)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.shares = validated_data.get('shares', instance.shares)
        instance.status = validated_data.get('status', instance.status)
        instance.image_post = validated_data.get('image_post', instance.image_post)
        instance.image_contents = validated_data.get('image_contents', instance.image_contents)
        instance.last_update = get_today()

        instance.save()
        return instance
