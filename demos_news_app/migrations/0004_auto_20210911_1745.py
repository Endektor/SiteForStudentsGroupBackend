# Generated by Django 3.0.7 on 2021-09-11 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demos_news_app', '0003_auto_20210911_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picture',
            field=models.ImageField(null=True, upload_to='demos_news_pictures/'),
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
    ]
