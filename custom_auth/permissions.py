from rest_framework import permissions
from .models import Group


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsGroupMember(permissions.BasePermission):
    message = 'Вы не состоите в данной группе'

    def has_permission(self, request, view):
        group = request.GET.get('group', None)
        if not group:
            self.message = 'Не была предоставлена группа'
            return False
        try:
            group = Group.objects.get(name=group)
        except Group.DoesNotExist:
            self.message = 'Данной группы не существует'
            return False

        return group in request.user.group.all()


class IsObjectInUsersGroup(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.group in request.user.group
