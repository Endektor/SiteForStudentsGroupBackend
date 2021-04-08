from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.core.validators import validate_unicode_slug
from django.db import models

import string
import random
import datetime
import copy
import base64
import os


class User(AbstractUser):
    pass


class Group(models.Model):
    name = models.CharField(unique=True, max_length=128, validators=[validate_unicode_slug])
    users = models.ManyToManyField(User, related_name='users_in_group', through='GroupPermission')

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        os.remove('mail_app/group_files/' + self.name + '/')
        super(Group, self).delete()


ROLES = [
    ('redactor', 'redactor'),
    ('user', 'user'),
]


class GroupPermission(models.Model):
    roles = copy.deepcopy(ROLES).append(('admin', 'admin'))

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_permission')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permission')
    role = models.CharField(choices=roles, default='user', max_length=20)


class GroupToken(models.Model):
    role = models.CharField(choices=ROLES, default='user', max_length=20)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_token')
    creation_time = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=32, null=True)

    def save(self, *args, **kwargs):
        letters = string.ascii_letters + string.digits
        today = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
        today_base64 = base64.b64encode(today.encode()).decode().replace('=', '')
        self.token = ''.join(random.choices(letters, k=10)) + today_base64
        super(GroupToken, self).save(*args, **kwargs)
