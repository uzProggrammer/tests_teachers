# Generated by Django 4.2.4 on 2023-08-14 16:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0016_draganddropquiz_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemultiquiz',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
