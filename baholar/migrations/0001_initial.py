# Generated by Django 4.1.3 on 2023-04-20 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assignments', '0004_remove_assignment_fan_assignment_is_readed_and_more'),
        ('bsb', '0015_bsbquizball_quizess_delete_bsbquizanswer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Baho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('baho', models.CharField(choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1'), ('0', '0'), ('DQ', 'Darsda qatnashmadi'), ('BO', 'Baho olmadi')], max_length=40)),
                ('assignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bahocalar', to='assignments.assignment')),
                ('bsb', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='baholarr', to='bsb.bsb')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baholar', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
