from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Group(models.Model):
    name = models.CharField(unique=True, max_length=128)
    users = models.ManyToManyField(User, related_name='users_in_group', through='GroupPermission')

    def __str__(self):
        return self.name


class GroupPermission(models.Model):
    roles = [
        ('admin', 'admin'),
        ('redactor', 'redactor'),
        ('user', 'user'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_permission')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permission')
    role = models.CharField(choices=roles, default='user', max_length=20)
