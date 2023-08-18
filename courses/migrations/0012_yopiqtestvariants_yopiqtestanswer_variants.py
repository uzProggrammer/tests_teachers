# Generated by Django 4.2.4 on 2023-08-14 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_quizanswer_variant'),
    ]

    operations = [
        migrations.CreateModel(
            name='YopiqTestVariants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('is_true', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='courses.courseyopiqtest')),
            ],
        ),
        migrations.AddField(
            model_name='yopiqtestanswer',
            name='variants',
            field=models.ManyToManyField(related_name='answers', to='courses.yopiqtestvariants'),
        ),
    ]