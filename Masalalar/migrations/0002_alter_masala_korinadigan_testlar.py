# Generated by Django 4.2.4 on 2023-08-19 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masalalar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masala',
            name='korinadigan_testlar',
            field=models.IntegerField(default=1),
        ),
    ]
