# Generated by Django 4.2.4 on 2023-08-30 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizess', '0009_closedtestanswer_user_result_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='StartedTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strted_time', to='quizess.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='started_time_in_quiz', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]