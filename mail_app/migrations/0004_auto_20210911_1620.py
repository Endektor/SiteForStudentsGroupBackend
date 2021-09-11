# Generated by Django 3.0.7 on 2021-09-11 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0003_auto_20210815_0029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attachment',
            options={'verbose_name': 'Вложение', 'verbose_name_plural': 'Вложения'},
        ),
        migrations.AlterModelOptions(
            name='letter',
            options={'verbose_name': 'Письмо', 'verbose_name_plural': 'Письма'},
        ),
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to='mail_attachments/', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='letter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='letter', to='mail_app.Letter', verbose_name='Письмо'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='date_time',
            field=models.DateTimeField(verbose_name='Дата и время отправления'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='mailer',
            field=models.CharField(max_length=128, verbose_name='Отправитель'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='text',
            field=models.TextField(blank=True, verbose_name='Тело письма'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='topic',
            field=models.CharField(blank=True, max_length=256, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='uid',
            field=models.IntegerField(unique=True, verbose_name='Уникальный id письма'),
        ),
    ]
