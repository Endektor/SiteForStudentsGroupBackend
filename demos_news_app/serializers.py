from rest_framework import serializers
from .models import Post, Tag

from custom_auth.models import User
from custom_auth.serializers import UserSerializer


class UserPostsSerializer(UserSerializer):
    """
    Serializer for getting user's posts
    """
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        ref_name = 'posts_user'
        model = User
        fields = ('id', 'username', 'posts')


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for getting tags
    """
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for getting post
    """
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'date', 'author', 'tags')
        depth = 1
