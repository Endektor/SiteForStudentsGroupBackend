from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(User, related_name='group')

    def __str__(self):
        return self.name
