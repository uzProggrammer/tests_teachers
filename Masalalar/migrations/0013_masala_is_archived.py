# Generated by Django 4.2.4 on 2023-08-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masalalar', '0012_masala_yechim'),
    ]

    operations = [
        migrations.AddField(
            model_name='masala',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
