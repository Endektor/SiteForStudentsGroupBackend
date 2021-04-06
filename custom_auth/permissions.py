from rest_framework import permissions
from .models import Group


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows to read for everyone and allows to change only for owner
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


class IsGroupRedactor(IsGroupMember):
    """
    Checks if user is admin or redactor of group
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
    The same as IsGroupRedactorOrReadOnly, but only for admin
    """
    role = ('admin',)


class IsGroupRedactorOrReadOnly(IsGroupRedactor):
    """
    Allows to read for member of group and to change for redactor and admin
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super(IsGroupRedactorOrReadOnly, self).has_permission(request, view)


class IsGroupAdminOrReadOnly(IsGroupRedactorOrReadOnly):
    """
    The same as IsGroupRedactorOrReadOnly, but only for admin
    """
    role = ('admin',)


def get_group(request):
    """
    Returns group from query parameters or from body
    """
    return request.GET.get('group', request.POST.get('group', None))
