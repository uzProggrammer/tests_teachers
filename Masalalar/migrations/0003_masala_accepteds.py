# Generated by Django 4.2.4 on 2023-08-19 17:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Masalalar', '0002_alter_masala_korinadigan_testlar'),
    ]

    operations = [
        migrations.AddField(
            model_name='masala',
            name='accepteds',
            field=models.ManyToManyField(related_name='masala_accepts', to=settings.AUTH_USER_MODEL),
        ),
    ]