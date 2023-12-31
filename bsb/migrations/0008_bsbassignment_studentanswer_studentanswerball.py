# Generated by Django 4.1.3 on 2023-04-04 16:05

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bsb', '0007_bsbproblemanswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='BsbAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('info', ckeditor.fields.RichTextField()),
                ('is_readed', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('max_ball', models.FloatField(default=2.0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bsb_assignment_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor.fields.RichTextField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='bsb.bsbassignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bsb_assignment_answers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswerBall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.FloatField()),
                ('student_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_balls', to='bsb.studentanswer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bsb_assignment_answer_balls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
