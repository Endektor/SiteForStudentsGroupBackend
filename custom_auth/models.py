from django.contrib.auth.models import AbstractUser
from django.db import models
import string
import random
import datetime
import copy


class User(AbstractUser):
    pass
    # class Meta:
    #     ref_name="test"


class Group(models.Model):
    name = models.CharField(unique=True, max_length=128)
    users = models.ManyToManyField(User, related_name='users_in_group', through='GroupPermission')

    def __str__(self):
        return self.name


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
        date = str(datetime.date.today()).replace('-', '')
        self.token = ''.join(random.choices(letters, k=20)) + date
        super(GroupToken, self).save(*args, **kwargs)


