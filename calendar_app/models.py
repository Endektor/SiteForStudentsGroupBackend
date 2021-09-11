from datetime import date
from django.db import models
from django.utils import timezone

from colorfield.fields import ColorField


class Day(models.Model):
    date = models.DateField("Дата", unique=True, default=date.today)
    topic = models.CharField("Заголовок", blank=True, max_length=256)

    def __str__(self):
        return f"{str(self.date.day)}/{str(self.date.month)}/{str(self.date.year)}"

    class Meta:
        verbose_name = "День"
        verbose_name_plural = "Дни"


class Event(models.Model):
    description = models.TextField("Описание", blank=True)
    day = models.ForeignKey(Day, verbose_name="День", null=True, on_delete=models.CASCADE, related_name="event")
    event_info = models.ForeignKey("Info", verbose_name="Тема события", null=True, on_delete=models.SET_NULL, related_name="event_info")
    time = models.TimeField("Время события", default=timezone.now)

    def __str__(self):
        return str(self.day)

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"


class Info(models.Model):
    color = ColorField("Цвет", default="#FF0000")
    topic = models.CharField("Тема", blank=True, max_length=256)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Тип события"
        verbose_name_plural = "Типы событий"
