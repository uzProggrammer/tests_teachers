# Generated by Django 4.1.3 on 2023-03-21 16:37

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('info', ckeditor.fields.RichTextField()),
                ('sinf', models.CharField(blank=True, choices=[('51', '5.1'), ('52', '5.2'), ('61', '6.1'), ('62', '6.2'), ('71', '7.1'), ('72', '7.2'), ('73', '7.3'), ('81', '8.1'), ('82', '8.2'), ('83', '8.3'), ('91', '9.1'), ('92', '9.2'), ('93', '9.3'), ('101', '10.1'), ('102', '10.2'), ('103', '10.3'), ('111', '11.1'), ('112', '11.2'), ('113', '11.3')], max_length=50, null=True)),
                ('fan', models.CharField(blank=True, choices=[('Ona Tili', 'Ona Tili'), ('Adabiyot', 'Adabiyot'), ('Algebra', 'Algebra'), ('Geometriya', 'Geometriya'), ('Geografiya', 'Geografiya'), ('Biologiya', 'Biologiya'), ('Ingliz tili', 'Ingliz tili'), ('Jismoniy tarbiya', 'Jismoniy tarbiya'), ('Tarbiya', 'Tarbiya'), ('Jahon tarixi', 'Jahon tarixi'), ("O'zbekiston tarixi", "O'zbekiston tarixi"), ('Kimyo', 'Kimyo'), ('Rus tili', 'Rus tili'), ('Musiqa', 'Musiqa'), ('Texnalogiya', 'Texnalogiya'), ('Darsdan tashqari', 'Darsdan tashqari')], max_length=50, null=True)),
                ('qachongacha', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('max_ball', models.FloatField(default=2.0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_author', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignment_student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', ckeditor.fields.RichTextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigment_answer', to='assignments.assignment')),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='student_answer_likes', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answer', to=settings.AUTH_USER_MODEL)),
                ('yordam_berganlar', models.ManyToManyField(blank=True, null=True, related_name='student_answer_helpers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswerBall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.FloatField()),
                ('xatolar_va_kamchiliklar', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='teacher_ball_likes', to=settings.AUTH_USER_MODEL)),
                ('student_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answer_ball', to='assignments.studentanswer')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_student_ball', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswerComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='student_answer_comments_likes', to=settings.AUTH_USER_MODEL)),
                ('student_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answer_comments', to='assignments.studentanswer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answer_comments_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswerBallComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('likes', models.ManyToManyField(blank=True, null=True, related_name='student_answer_ball_comment_likes', to=settings.AUTH_USER_MODEL)),
                ('student_answer_ball', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answer_ball_comment', to='assignments.studentanswerball')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_answer_ball_comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]