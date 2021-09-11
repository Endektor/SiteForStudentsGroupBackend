from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Post, Tag


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", default=timezone.now)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'date', 'author', 'tags', 'picture')
        depth = 1
