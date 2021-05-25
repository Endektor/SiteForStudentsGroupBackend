from django.contrib.auth.models import User
from django.db import models


class BlackList(models.Model):
    refresh_token = models.CharField(max_length=128)

    def __str__(self):
        return self.refresh_token


class WhiteList(models.Model):
    refresh_token = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.refresh_token
