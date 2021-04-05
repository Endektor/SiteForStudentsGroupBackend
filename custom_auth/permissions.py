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
    message = 'You are not group member'

    def has_permission(self, request, view):
        group = get_group(request)
        if not group:
            self.message = 'Group has not been provided'
            return False
        try:
            group = Group.objects.get(name=group)
        except Group.DoesNotExist:
            self.message = 'Group does not exist'
            return False

        return group in request.user.users_in_group.all()


class IsObjectInUsersGroup(permissions.BasePermission):
    """
    Check if object is in user's group
    """
    def has_object_permission(self, request, view, obj):
        return obj.group in request.user.users_in_group


class IsGroupRedactor(IsGroupMember):
    """
    Checks if user has redactor or admin role in group
    """
    role = ('admin', 'redactor')
    message = 'User does not have the required role'

    def has_permission(self, request, view):
        success = super(IsGroupRedactor, self).has_permission(request, view)
        if not success:
            return False
        group = Group.objects.get(name=get_group(request))
        return request.user.user_permission.get(group=group.id).role in self.role


class IsGroupAdmin(IsGroupRedactor):
    """
    Checks if user has admin role in group
    """
    role = ('admin',)


def get_group(request):
    """
    Returns group from query parameters or from body
    """
    return request.GET.get('group', request.POST.get('group', None))