# Generated by Django 4.1.3 on 2023-03-08 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_myuser_fan_alter_myuser_sinf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='bio',
            field=models.TextField(default='.'),
        ),
    ]
