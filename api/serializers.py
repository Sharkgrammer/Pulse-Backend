from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.functions.functions import get_today
from api.models import Post, User, Follow, Like, Comment, Interest, Interest_User


class PostSerializer(serializers.Serializer):
    pid = serializers.CharField(read_only=True)
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
    profile_name = serializers.CharField(source="created_by.get_name", read_only=True)
    profile_username = serializers.CharField(source="created_by.username", read_only=True)
    profile_image = serializers.ImageField(source="created_by.prof_image", read_only=True)
    liked = SerializerMethodField(method_name='get_liked', read_only=True)

    def validate_image_contents(self, image):
        # TODO validate image here
        print("Waiting image validation")

    def get_liked(self, post):
        return Like.objects.filter(post__id=post.id, created_by=self.context.get("user"), deleted=False).exists()

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


class UserSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    first_name = serializers.CharField(default="")
    last_name = serializers.CharField(default="")
    email = serializers.EmailField(default="")
    username = serializers.CharField(default="")
    prof_image = serializers.ImageField(default="")
    prof_desc = serializers.CharField(default="")
    followers = serializers.IntegerField(default=0)
    following = serializers.IntegerField(default=0)
    date_joined = serializers.DateTimeField(required=False)
    last_login = serializers.DateTimeField(required=False)
    following_user = SerializerMethodField(method_name='is_following_me', read_only=True)

    def is_following_me(self, user):
        main_user = self.context.get("user")

        if user == main_user or main_user is None:
            return False

        return Follow.objects.filter(created_by=main_user, following=user, deleted=False).exists()

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('exclude_fields', [])

        for field in exclude_fields:
            fields.pop(field, default=None)

        return fields

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.prof_image = validated_data.get('prof_image', instance.prof_image)
        instance.prof_desc = validated_data.get('prof_desc', instance.prof_desc)
        instance.followers = validated_data.get('followers', instance.followers)
        instance.following = validated_data.get('following', instance.following)
        instance.date_joined = validated_data.get('image_post', instance.date_joined)
        instance.last_login = validated_data.get('image_contents', instance.last_login)

        instance.save()
        return instance


class FollowSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    following_username = serializers.CharField(source="following.username", read_only=True)
    created_date = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Follow.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.following = validated_data.get('following', instance.following)

        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    post_id = serializers.CharField(source="post.pid", read_only=True)
    content = serializers.CharField(default="")
    likes = serializers.IntegerField(default=0)
    profile_name = serializers.CharField(source="created_by.get_name", read_only=True)
    profile_username = serializers.CharField(source="created_by.username", read_only=True)
    profile_image = serializers.ImageField(source="created_by.prof_image", read_only=True)
    created_date = serializers.DateTimeField(required=False)
    liked = SerializerMethodField(method_name='get_liked', read_only=True)

    def get_liked(self, comment):
        return Like.objects.filter(comment_id=comment.id, created_by=self.context.get("user"), deleted=False).exists()

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.post = validated_data.get('post', instance.post)
        instance.content = validated_data.get('content', instance.content)
        instance.likes = validated_data.get('likes', instance.likes)

        instance.save()
        return instance


class LikeSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)
    post_id = serializers.CharField(source="post.pid", read_only=True)
    comment_id = serializers.CharField(source="comment.id", read_only=True)
    created_date = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return Like.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.post = validated_data.get('post', instance.post)
        instance.comment = validated_data.get('comment', instance.comment)

        instance.save()
        return instance


class InterestSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=255)
    count = serializers.IntegerField(default=0)
    interested = SerializerMethodField(method_name='get_user_interested', read_only=True)

    def get_user_interested(self, interest):
        return Interest_User.objects.filter(interest=interest, user=self.context.get("user"), deleted=False).exists()

    def create(self, validated_data):
        return Interest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.count = validated_data.get('count', instance.post)

        instance.save()
        return instance
