from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers

from .models import Group, GroupPermission


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'group_user'
        model = User
        fields = ('id', 'username')


class GroupSerializer(serializers.ModelSerializer):
    # users = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'users')


class GroupPermissionSerializer(serializers.ModelSerializer):
    # group = GroupSerializer()

    class Meta:
        model = GroupPermission
        fields = ('id', 'group', 'user', 'role')


class GetGroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'users')


class GetGroupPermissionSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    user = UserSerializer(many=True)

    class Meta:
        model = GroupPermission
        fields = ('id', 'group', 'user', 'role')
