# Generated by Django 3.0.7 on 2021-08-13 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='uid',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
