# Generated by Django 3.0.7 on 2021-11-01 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demos_news_app', '0004_auto_20210911_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='demos_news_pictures/'),
        ),
    ]
