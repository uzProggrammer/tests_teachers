# Generated by Django 4.2.4 on 2023-08-14 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_alter_coursemultiquiz_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiquizanswer',
            name='variants',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='courses.multiquizvariuant'),
            preserve_default=False,
        ),
    ]