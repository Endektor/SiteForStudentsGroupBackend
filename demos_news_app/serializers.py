from rest_framework import serializers
from .models import Post, Tag
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'post')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'date', 'author', 'tag')
        depth = 1



