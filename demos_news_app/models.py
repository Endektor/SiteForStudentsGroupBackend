from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(blank=True)
    date = models.DateTimeField(unique=True, default=timezone.now)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')
    picture = models.ImageField(blank=True, null=True, upload_to="demos_news_pictures/")

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    post = models.ManyToManyField(Post, related_name='tags', blank=True)

    def __str__(self):
        return self.name
