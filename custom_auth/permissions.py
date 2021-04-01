from rest_framework import permissions
from .models import Group


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows to read for everyone and allows to change only for admin
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsGroupMember(permissions.BasePermission):
    """
    Check if user is in group
    """
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

        return group in request.user.users_in_group.all()


class IsObjectInUsersGroup(permissions.BasePermission):
    """
    Check if object is in user's group
    """
    def has_object_permission(self, request, view, obj):
        return obj.group in request.user.users_in_group


class IsGroupRole(IsGroupMember):
    """
    Check if user has a role in group
    """
    role = None

    def has_permission(self, request, view):
        success = super(IsGroupRole, self).has_permission(request, view)
        if not success:
            return False
        group = request.GET.get('group', None)
        group = Group.objects.get(name=group)
        return request.user.user_permission.get(group=group.id).role == self.role


class IsGroupAdmin(IsGroupRole):
    role = 'admin'


class IsGroupRedactor(IsGroupRole):
    role = 'redactor'
