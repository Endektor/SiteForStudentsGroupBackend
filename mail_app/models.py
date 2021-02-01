from django.db import models
from datetime import date
from django.utils import timezone


class Letter(models.Model):
    mailer = models.CharField(max_length=128)
    topic = models.CharField(blank=True, max_length=256)
    text = models.TextField(blank=True)
    date_time = models.DateTimeField()

    def __str__(self):
        return self.topic


class Attachment(models.Model):
    file = models.FileField(upload_to='mail_attachments/')
    letter = models.ForeignKey('Letter', on_delete=models.CASCADE, null=True, related_name='letter')
