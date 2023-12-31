# Generated by Django 4.1.3 on 2023-04-04 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bsb', '0006_bsbproblem_bsbproblemball_remove_bsbball_bsb_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BsbProblemAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('type', models.CharField(max_length=30)),
                ('bsb_problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='bsb.bsbproblem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bsb_task_answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
