# Generated by Django 4.1.2 on 2023-06-07 17:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_update_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
