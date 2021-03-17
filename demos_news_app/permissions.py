from rest_framework import permissions
from custom_auth.models import Group


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsGroupMember(permissions.BasePermission):
    def has_permission(self, request, view):
        group = request.GET.get('group', None)
        group = Group.objects.get(name=group)

        return group in request.user.group.all()


class IsObjectInUsersGroup(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.group in request.user.group
