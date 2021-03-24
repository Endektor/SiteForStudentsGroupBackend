from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers

from .models import Group, GroupPermission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'users')


class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'users')


class GroupPermissionSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = GroupPermission
        fields = ('id', 'group', 'user', 'role')
