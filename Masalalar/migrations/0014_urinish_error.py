# Generated by Django 4.2.4 on 2023-08-22 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Masalalar', '0013_masala_is_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='urinish',
            name='error',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]