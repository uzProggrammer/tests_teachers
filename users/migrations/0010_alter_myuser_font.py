# Generated by Django 4.1.3 on 2023-04-22 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_myuser_font'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='font',
            field=models.CharField(default='sans-serif', max_length=30),
        ),
    ]
