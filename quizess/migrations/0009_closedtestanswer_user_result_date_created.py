# Generated by Django 4.2.4 on 2023-08-30 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizess', '0008_closedtest_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedtestanswer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='closed_test_answers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]