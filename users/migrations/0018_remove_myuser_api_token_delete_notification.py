# Generated by Django 4.2.4 on 2023-11-07 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_notification_is_readed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='api_token',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]