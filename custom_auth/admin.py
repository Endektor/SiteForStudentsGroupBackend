from django.contrib import admin
from .models import Group, GroupPermission, User, GroupToken
from django.contrib.auth.admin import UserAdmin


class GroupPermissionInline(admin.TabularInline):
    model = GroupPermission
    extra = 0


class GroupAdmin(admin.ModelAdmin):
    inlines = [
        GroupPermissionInline,
    ]


class GroupTokenAdmin(admin.ModelAdmin):
    # list_display = ('creation_time',)
    pass
    # exclude = ['token']


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupPermission)
admin.site.register(User, UserAdmin)
admin.site.register(GroupToken, GroupTokenAdmin)
