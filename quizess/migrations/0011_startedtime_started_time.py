# Generated by Django 4.2.4 on 2023-08-30 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizess', '0010_startedtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='startedtime',
            name='started_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
