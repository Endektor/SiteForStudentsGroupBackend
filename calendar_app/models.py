from django.db import models
from datetime import date
from django.utils import timezone
from colorfield.fields import ColorField
from custom_auth.models import Group


class Day(models.Model):
    date = models.DateField(unique=True, default=date.today)
    topic = models.CharField(blank=True, max_length=256)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_day')

    def __str__(self):
        return f'{str(self.date.day)}/{str(self.date.month)}/{str(self.date.year)}'


class Event(models.Model):
    description = models.TextField(blank=True)
    day = models.ForeignKey('Day', null=True, on_delete=models.CASCADE, related_name='day_event')
    info = models.ForeignKey('Info', null=True, on_delete=models.SET_NULL, related_name='info_event')
    time = models.TimeField(default=timezone.now)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_event')

    def __str__(self):
        return str(self.day)


class Info(models.Model):
    color = ColorField(default='#FF0000')
    topic = models.CharField(blank=True, max_length=256)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_info')

    def __str__(self):
        return self.topic
