# Generated by Django 4.1.3 on 2023-03-21 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswerballcomment',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentanswercomments',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
