# Generated by Django 4.2.4 on 2023-08-13 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_coursequiz_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='draganddropanswer',
            name='lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='course_drag_anddrop_answers', to='courses.lessons'),
            preserve_default=False,
        ),
    ]
