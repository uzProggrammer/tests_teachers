# Generated by Django 4.2.4 on 2023-09-01 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizess', '0011_startedtime_started_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='orin',
            field=models.IntegerField(default=1),
        ),
    ]