# Generated by Django 4.2.4 on 2023-08-13 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_yopiqtestanswer_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizanswer',
            name='lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='course_quiz_answer', to='courses.lessons'),
            preserve_default=False,
        ),
    ]
