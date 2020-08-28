from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(blank=True)
    date = models.DateTimeField(unique=True, default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    post = models.ManyToManyField(Post, related_name='post')

    def __str__(self):
        return self.name
