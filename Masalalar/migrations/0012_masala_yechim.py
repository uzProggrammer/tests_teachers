# Generated by Django 4.2.4 on 2023-08-21 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masalalar', '0011_masala_have_yechim'),
    ]

    operations = [
        migrations.AddField(
            model_name='masala',
            name='yechim',
            field=models.TextField(blank=True, null=True),
        ),
    ]
