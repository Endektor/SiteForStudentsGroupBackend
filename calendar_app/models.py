from django.db import models
from datetime import date
from django.utils import timezone
from colorfield.fields import ColorField


class Day(models.Model):
    date = models.DateField(unique=True, default=date.today)
    topic = models.CharField(blank=True, max_length=256)

    def __str__(self):
        return f'{str(self.date.day)}/{str(self.date.month)}/{str(self.date.year)}'

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'


class Event(models.Model):
    description = models.TextField(blank=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='event')
    event_info = models.ForeignKey('Info', null=True, on_delete=models.SET_NULL, related_name='event_info')
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return str(self.day)


class Info(models.Model):
    color = ColorField(default='#FF0000')
    topic = models.CharField(blank=True, max_length=256)

    def __str__(self):
        return self.topic
