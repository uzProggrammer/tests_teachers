# Generated by Django 4.1.3 on 2023-04-17 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bsb', '0013_alter_bsbquizball_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='BsbQuizAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.FloatField()),
                ('quizess', models.ManyToManyField(related_name='quiz_answers', to='bsb.bsbquiztests')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bsb_quiz_answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
