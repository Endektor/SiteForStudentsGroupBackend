from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.serializers import UserCreateSerializer
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
    posts = serializers.SerializerMethodField()

    def get_posts(self, obj):
        ordered_queryset = obj.posts.order_by('-date') 
        return PostSerializer(ordered_queryset, many=True, context=self.context).data
    
    class Meta:
        model = User
        fields = ('id', 'username', 'posts', 'email')
        depth = 0


class DjoserUserSerializer(UserCreateSerializer):

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        email = attrs.get("email")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Пользователь с таким почтовым адресом уже зарегистрирован, но я тебе этого не говорил, хорошо?)"}
            )

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs
