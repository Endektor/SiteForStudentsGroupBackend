# Generated by Django 3.0.7 on 2021-09-11 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demos_news_app', '0002_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='picture',
            new_name='file',
        ),
        migrations.AlterField(
            model_name='picture',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_picture', to='demos_news_app.Post'),
        ),
    ]
