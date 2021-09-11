from django.db import models


class Letter(models.Model):
    mailer = models.CharField("Отправитель", max_length=128)
    topic = models.CharField("Заголовок", blank=True, max_length=256)
    text = models.TextField("Тело письма", blank=True)
    date_time = models.DateTimeField("Дата и время отправления", )
    uid = models.IntegerField("Уникальный id письма", unique=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"


class Attachment(models.Model):
    file = models.FileField("Файл", upload_to="mail_attachments/")
    letter = models.ForeignKey('Letter', verbose_name="Письмо", on_delete=models.CASCADE, null=True, related_name="letter")

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"