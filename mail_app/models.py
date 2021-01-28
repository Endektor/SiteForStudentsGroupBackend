from django.db import models
from datetime import date
from django.utils import timezone


class Letter(models.Model):
    mailer = models.CharField(max_length=128)
    topic = models.CharField(blank=True, max_length=256)
    text = models.TextField(blank=True)

    def __str__(self):
        return self.topic
