# Generated by Django 4.2.4 on 2023-08-19 18:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Masalalar', '0003_masala_accepteds'),
    ]

    operations = [
        migrations.AddField(
            model_name='masala',
            name='wrong_answers',
            field=models.ManyToManyField(blank=True, null=True, related_name='masala_wrongs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='masala',
            name='accepteds',
            field=models.ManyToManyField(blank=True, null=True, related_name='masala_accepts', to=settings.AUTH_USER_MODEL),
        ),
    ]
