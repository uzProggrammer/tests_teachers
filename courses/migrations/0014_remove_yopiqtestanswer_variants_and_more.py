# Generated by Django 4.2.4 on 2023-08-14 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_remove_yopiqtestanswer_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yopiqtestanswer',
            name='variants',
        ),
        migrations.DeleteModel(
            name='YopiqTestVariants',
        ),
    ]
