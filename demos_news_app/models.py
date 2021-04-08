from django.db import models
from django.utils import timezone
from django.conf import settings

from custom_auth.models import Group


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(blank=True)
    date = models.DateTimeField(unique=True, default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_post')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    post = models.ManyToManyField(Post, related_name='post_tags')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_tag')

    def __str__(self):
        return self.name
