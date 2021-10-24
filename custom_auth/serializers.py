from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers

from demos_news_app.models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    date = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", default=timezone.now)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'date', 'tags', 'picture')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')
        depth = 0
