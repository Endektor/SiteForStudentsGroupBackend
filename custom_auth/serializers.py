from rest_framework import serializers

from .models import Group, GroupPermission, User, GroupToken


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for swagger auth
    """
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'group_user'
        model = User
        fields = ('id', 'username')


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for creating group
    """
    class Meta:
        model = Group
        fields = ('id', 'name', 'users')


class GetGroupSerializer(GroupSerializer):
    """
    Serializer for getting group
    """
    users = UserSerializer(many=True)


class GroupPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for creating group permission
    """
    class Meta:
        model = GroupPermission
        fields = ('id', 'group', 'user', 'role')


class GetGroupPermissionSerializer(GroupPermissionSerializer):
    """
    Serializer for getting group permission
    """
    group = GroupSerializer()
    user = UserSerializer(many=True)


class GroupTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupToken
        fields = ('id', 'role', 'group', 'creation_time', 'token')
